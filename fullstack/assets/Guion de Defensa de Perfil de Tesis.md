
> [!IMPORTANT]
> Actualmente la colección `modalities` en Firestore almacena las **modalidades de ingreso**. Para las **modalidades de graduación** necesitamos crear una nueva colección `graduation_modalities` con un tipo e interfaz propia. ¿Está bien este nombre o prefieres otro?

> [!IMPORTANT]
> El acceso admin se controla vía `useProtectedRoute()` (verifica `isAuthenticated` de Firebase Auth). ¿Es suficiente considerar que cualquier usuario autenticado con Firebase es admin, o necesitas un rol específico (ej. un campo `role: "admin"` en Firestore)?

---
# Architectural Refactor: Separate Business Logic from React Components

The codebase has a recurring pattern where React components contain **all the business logic inline** — data transformation, submission orchestration, toast notifications, navigation, error handling — mixed directly with JSX. This makes components hard to read, hard to test, and produces massive amounts of duplication across modules.

This plan proposes a **hooks-first refactor** that extracts business logic into custom hooks while leaving components as thin rendering shells.

## Diagnosis: What's Wrong Today

### 1. Massive copy-paste across report modules
`student.tsx`, `graduates.tsx`, `scholarship.tsx`, and `teacher.tsx` are **~95% identical**. The only differences between the first three are:
- The module name string (`'student'` / `'graduate'` / `'scholarships'`)
- The confirmation dialog message (`"Estudiantes"` / `"Egresados"` / `"Becas"`)

This is ~450 lines of duplicated code across 3 files that do the exact same thing.

### 2. Components own business logic they shouldn't
Every report component contains:
- Data transformation logic (`Object.entries(data).reduce(...)`)
- Submission orchestration (mutateAsync → markStepCompleted → navigation)
- Toast notifications (success, error, completion)
- Column definition for tables (in teacher/responses panel)

None of this belongs in a React component — it's pure business logic that should be testable without rendering anything.

### 3. Hooks live in `shared/` when they belong to features
`useFormBuilder.ts`, `useFormResponses.ts`, `useDirectorProgress.ts`, and `useNextFormRoute.ts` are all in `shared/hooks/`, but they are **exclusively used by the reports feature**. Per the project's own `feature-architecture.md`, these should live inside `features/reports/` until they're needed elsewhere.

### 4. No separation between "data access" and "workflow" hooks
Hooks like `useSubmitFormResponse` do raw Firestore operations **and** toast notifications **and** query invalidation all in one place. This couples infrastructure to UX feedback.

---

## Proposed Changes

### Layer 1: Reports Feature — Eliminate Duplication

The three single-submit report modules (`student`, `graduates`, `scholarship`) will be replaced by a **single generic component** + a **shared custom hook**.

#### [NEW] `src/features/reports/hooks/useReportSubmission.ts`

A custom hook that encapsulates the entire submit workflow shared by all single-submit reports:

```typescript
// Extracts: data transformation, mutation, step completion, navigation, toast notifications
export function useReportSubmission(module: string, formId: string) {
  // Hooks
  const { mutateAsync } = useSubmitFormResponse();
  const { mutateAsync: markStepCompleted } = useMarkStepCompleted();
  const { profile } = useDirectorProfile();
  const navigate = useNavigate();
  const nextUrl = useGetNextTemplateUrl(formId);

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [pendingData, setPendingData] = useState<...>(null);

  // Actions
  const requestSubmit = (data, module) => { ... };
  const confirmSubmit = async () => { ... };
  const cancelSubmit = () => { ... };

  return { isDialogOpen, setIsDialogOpen, requestSubmit, confirmSubmit, cancelSubmit };
}
```

This single hook replaces the **identical** `handleFormSubmitRequest` + `executeSubmit` logic duplicated in 3 files today.

---

#### [NEW] `src/features/reports/components/SingleSubmitReport.tsx`

A generic component that renders any single-submit report form (student, graduate, scholarship):

```tsx
interface SingleSubmitReportProps {
  formId: string;
  module: string;             // 'student' | 'graduate' | 'scholarships'
  confirmationEntity: string; // 'Estudiantes' | 'Egresados' | 'Becas'
}
```

This replaces `student.tsx`, `graduates.tsx`, and `scholarship.tsx` — going from ~450 lines → ~60 lines.

---

#### [MODIFY] `src/features/reports/student.tsx`

Becomes a thin wrapper:
```tsx
export function StudentReport({ formId }) {
  return <SingleSubmitReport formId={formId} module="student" confirmationEntity="Estudiantes" />;
}
```

#### [MODIFY] `src/features/reports/graduates.tsx`

Same pattern — thin wrapper around `SingleSubmitReport`.

#### [MODIFY] `src/features/reports/scholarship.tsx`

Same pattern — thin wrapper around `SingleSubmitReport`.

---

#### [NEW] `src/features/reports/hooks/useTeacherBulkSubmission.ts`

Extracts the teacher-specific bulk submission logic (add-to-memory, bulk upload, column definitions) from `teacher.tsx`:

```typescript
export function useTeacherBulkSubmission(formId: string) {
  // All the state: teachers[], isDialogOpen, columns
  // All the actions: handleAddTeacherToMemory, executeSubmitBulk
  return { teachers, columns, isDialogOpen, addTeacher, submitAll, ... };
}
```

#### [MODIFY] `src/features/reports/teacher.tsx`

Becomes a **rendering-only** component (~80 lines of JSX, zero business logic):

```tsx
export function TeacherReport({ formId }) {
  const { template, isPending, isError, error } = useFormTemplateByModuleAndId('teacher', formId);
  const { teachers, columns, isDialogOpen, ... } = useTeacherBulkSubmission(formId);

  if (isPending) return <DynamicReportPageSkeleton />;
  // ... just JSX, no logic
}
```

---

### Layer 2: Relocate Feature-Specific Hooks

Move hooks that are **exclusively used by reports** from `shared/hooks/` into `features/reports/hooks/`. This follows the project's own architecture rules.

#### [MOVE] Hooks relocation

| Current Path | New Path | Reason |
|---|---|---|
| `shared/hooks/useFormBuilder.ts` | **Keep in `shared/`** | Used by `dashboard` AND `reports` |
| `shared/hooks/useFormResponses.ts` | **Keep in `shared/`** | Used by `dashboard/ResponsesPanel` AND `reports` |
| `shared/hooks/useDirectorProgress.ts` | `features/reports/hooks/useDirectorProgress.ts` | Only used by report modules |
| `shared/hooks/useNextFormRoute.ts` | `features/reports/hooks/useNextFormRoute.ts` | Only used by report modules |

> [!IMPORTANT]
> Moving hooks requires updating **all import paths** across the codebase. I will do a full grep to ensure no import is missed.

---

### Layer 3: Utility Extraction

#### [NEW] `src/features/reports/utils/transformFormData.ts`

The `Object.entries(data).reduce(...)` key-splitting pattern is duplicated in **every report file**. Extract it:

```typescript
/** Transforms form key format "fieldId@fieldName" → { fieldName: value } */
export function transformFormData(data: Record<string, unknown>): Record<string, unknown> {
  return Object.entries(data).reduce((acc, [key, value]) => {
    const [_id, name] = key.split('@');
    acc[name || key] = value;
    return acc;
  }, {} as Record<string, unknown>);
}
```

---

## Summary of File Changes

| Action     | File                                                              | Lines Before → After |
| ---------- | ----------------------------------------------------------------- | -------------------- |
| **NEW**    | `features/reports/hooks/useReportSubmission.ts`                   | — → ~70              |
| **NEW**    | `features/reports/hooks/useTeacherBulkSubmission.ts`              | — → ~90              |
| **NEW**    | `features/reports/components/SingleSubmitReport.tsx`              | — → ~60              |
| **NEW**    | `features/reports/utils/transformFormData.ts`                     | — → ~10              |
| **MODIFY** | `features/reports/student.tsx`                                    | 151 → ~10            |
| **MODIFY** | `features/reports/graduates.tsx`                                  | 150 → ~10            |
| **MODIFY** | `features/reports/scholarship.tsx`                                | 149 → ~10            |
| **MODIFY** | `features/reports/teacher.tsx`                                    | 242 → ~80            |
| **MOVE**   | `shared/hooks/useDirectorProgress.ts` → `features/reports/hooks/` | same                 |
| **MOVE**   | `shared/hooks/useNextFormRoute.ts` → `features/reports/hooks/`    | same                 |

**Net result:** ~690 lines of report code → ~340 lines, with zero duplication and fully testable business logic.

---

## What This Does NOT Change

- **`shared/ui/`** — Shadcn components stay untouched
- **`shared/components/`** — `DynamicForm`, `FormContainer`, etc. stay as-is
- **`features/dashboard/`** — CRUD screens are a separate concern (could be refactored later with the same pattern, but out of scope)
- **`features/auth/`** — Already has clean separation with hooks/providers/components
- **Route files** — Already thin, no changes needed
- **Firebase hooks** (`useFormBuilder`, `useFormResponses`) — Stay in `shared/` since they're used by multiple features

## Open Questions

> [!IMPORTANT]
> **Export style:** The current report modules are imported by route files like `import { TeacherReport } from '#/features/reports/teacher'`. After refactoring, should we keep these thin wrappers in the same files, or would you prefer a barrel `index.ts` per feature?

> [!IMPORTANT]
> **Dashboard CRUDs:** The same pattern of "component owns all logic" exists in `FacultiesCrud.tsx`, `ProgramsCrud.tsx`, etc. (~40K total). Want me to include those in this refactor, or tackle them in a separate pass?

## Verification Plan

### Automated Tests
```bash
pnpm check   # Biome lint + format validation
pnpm build   # Full TypeScript compilation — catches all broken imports
```

### Manual Verification
- Run `pnpm dev` and navigate each report route (`student-report`, `graduates-report`, `teacher-report`, `scholarship-report`) to verify form rendering and submission still works
- Verify the teacher bulk-add flow (add to table → bulk submit)
- Verify the dashboard `ResponsesPanel` still loads correctly (ensures `shared/hooks` aren't broken)

---                                                                                                                                                                                                                             
1. [ ] Controller Hooks Pattern                                                                                                                                                                                                       
      Extract all logic (state, handlers, API calls) into a single custom hook per component (e.g., useGraduatesReport.ts). The component only receives props and renders JSX.                                                          
 2. [ ] Service/Repository Pattern                                                                                                                                                                                                     
      Move complex business logic, data transformations, and API calls into pure TypeScript files (e.g., reportService.ts). Components/Hooks only handle React-specific state and UI logic.                                             
 3. [ ] State Management Refinement                                                                                                                                                                                                    
       Extract complex local state management into useReducer or a lightweight library (like Zustand) outside the component, keeping TanStack Query strictly for server state.
4. [ ] Container/Presentational Pattern                                                                                                                                                                                               
       Organize components into "Container" (smart components that fetch data and hold logic) and "Presentational" (dumb components that only render UI based on props).                                                                 
5. [ ] All of the above                                                                                                                                                                                                               
       Select all options                                                                                                                                                                                                                
 6. [ ] Enter a custom value         