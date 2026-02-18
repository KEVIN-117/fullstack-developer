# Class Student:

```C#
namespace MicrosoftFullStack.AcademicManagementSystem;

public class Student

{

    private Guid id;

    private string name;

    private Dictionary<string, Rating> courseRatings;

    private double averageRating;

    

    public Student(string name)

    {

        this.id = Guid.NewGuid();

        this.name = name;

        this.courseRatings = new Dictionary<string, Rating>();

        this.averageRating = 0;

    }

    

    public Guid Id => id;

    

    public string Name

    {

        get => name;

        set => name = value ?? throw new ArgumentNullException(nameof(value));

    }

    

    public double AverageRating => averageRating;

    

    public void AddCourseRating(string courseName, Rating rating)

    {

        if (string.IsNullOrEmpty(courseName))

        {

            throw new ArgumentException("Course name cannot be null or empty.", nameof(courseName));

        }


        courseRatings[courseName] = rating ?? throw new ArgumentNullException(nameof(rating));

        CalculateAverage();

    }

    

    public Rating? GetCourseRating(string? courseName)

    {

        if (string.IsNullOrEmpty(courseName))

        {

            throw new ArgumentException("Course name cannot be null or empty.", nameof(courseName));

        }


        return courseRatings.GetValueOrDefault(courseName);

    }


    public Dictionary<string, Rating> GetCourseRatings()

    {

        return courseRatings;

    }


    public void CalculateAverage()

    {

        

        foreach (var rating in courseRatings.Values)

        {

            // Assuming Rating has a method GetNumericValue() that returns a double

            averageRating += rating.RatingValue;

        }

        averageRating /= courseRatings.Count;

    }

}
```


# Class Rating:

```C#

namespace MicrosoftFullStack.AcademicManagementSystem;


public class Rating

{

    private string subject;

    private double rating;


    public Rating(string subject, double rating)

    {

        this.subject = subject ?? throw new ArgumentNullException(nameof(subject));

        this.rating = rating;

    }

    

    public string Subject

    {

        get => subject;

        set => subject = value ?? throw new ArgumentNullException(nameof(value));

    }

    

    public double RatingValue

    {

        get => rating;

        set => rating = value;

    }

}

```


# Class ManagementSystem:

```C#

using System.Text.Json;
namespace MicrosoftFullStack.AcademicManagementSystem;


public class ManagementSystem

{
    private List<Student>? _studentsList;

    public ManagementSystem()

    {
        _studentsList = new List<Student>();
    }

    public void AddStudent(Student student)
    {

        if (student == null)

        {

            throw new ArgumentNullException(nameof(student));

        }

        _studentsList.Add(student);

    }

    

    public void AddRating(Guid studentId, string courseName, Rating rating)

    {

        var student = _studentsList.FirstOrDefault(s => s.Id == studentId);

        if (student == null)

        {

            throw new ArgumentException("Student not found.", nameof(studentId));

        }

        student.AddCourseRating(courseName, rating);

    }

    

    public List<Student> GetAllRegistration()

    {

        return _studentsList;

    }

   

    public Student? GetRegistration(Guid studentId)

    {

        var student = _studentsList.FirstOrDefault(s => s.Id == studentId);

        return  student;

    }

    public void LoadData(string filePath)

    {

        string fullPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, filePath);


        if (File.Exists(fullPath))

        {

            string json = File.ReadAllText(fullPath);

            _studentsList = JsonSerializer.Deserialize<List<Student>>(json, new JsonSerializerOptions

            {

                PropertyNameCaseInsensitive = true

            });

        }

    }

    public void SaveData(string filePath)

    {

        string fullPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, filePath);

        string json = JsonSerializer.Serialize(_studentsList, new JsonSerializerOptions

        {

            WriteIndented = true

        });

        File.WriteAllText(fullPath, json);

    }

}

```

# Class Program:

```C#

using System.Globalization;

using Spectre.Console;


namespace MicrosoftFullStack.AcademicManagementSystem;


public class Program

{

    private const string ColorPrimary  = "cyan1";

    private const string ColorAccent   = "magenta1";

    private const string ColorSuccess  = "green1";

    private const string ColorWarning  = "yellow1";

    private const string ColorDanger   = "red1";

    private const string ColorMuted    = "grey50";


    public static void Main()

    {

        Program program = new Program();

        program.Run();

    }


    public void Run()

    {

        ManagementSystem managementSystem = new ManagementSystem();

        managementSystem.LoadData("students.json");

        SeedData(managementSystem);

        ShowBanner();

        ShowMenu(managementSystem);

    }


    public void SeedData(ManagementSystem managementSystem)

    {

        var seed = new (string Name, (string Course, double Score)[] Ratings)[]

        {

            ("Alice",   new[] { ("Mathematics", 4.5), ("Physics", 3.8) }),

            ("Bob",     new[] { ("Chemistry", 4.0),   ("Biology", 4.2) }),

            ("Carlos",  new[] { ("History", 3.9),     ("Literature", 4.7) }),

            ("Diana",   new[] { ("Computer Science", 4.8), ("Mathematics", 4.6) }),

            ("Ethan",   new[] { ("Economics", 3.5),   ("Statistics", 4.1) }),

            ("Fatima",  new[] { ("Philosophy", 4.3),  ("Sociology", 3.7) }),

            ("Gabriel", new[] { ("Art", 4.9),         ("Music", 4.6) }),

            ("Hannah",  new[] { ("Biology", 4.4),     ("Chemistry", 3.6) }),

            ("Ivan",    new[] { ("Physics", 4.2),     ("Computer Science", 4.7) }),

            ("Julia",   new[] { ("Literature", 4.8),  ("History", 4.0) }),

        };


        foreach (var (name, ratings) in seed)

        {

            var student = new Student(name);

            foreach (var (course, score) in ratings)

                student.AddCourseRating(course, new Rating(course, score));

            managementSystem.AddStudent(student);

        }

    }


    // ── Banner ────────────────────────────────────────────────────────────────

    private void ShowBanner()

    {

        AnsiConsole.Clear();


        // Dos líneas para que no se desborde en terminales estrechas

        AnsiConsole.Write(new FigletText("Academic Management System").Centered().Color(Color.Cyan1));

        AnsiConsole.Write(new FigletText("(SGA) - Student Grades").Centered().Color(Color.CadetBlue));


        AnsiConsole.Write(

            new Rule($"[{ColorMuted}]Academic Management System · v1.0 · Powered by Spectre.Console[/]")

                .RuleStyle(ColorMuted)

                .Centered());


        AnsiConsole.WriteLine();

    }


    // ── Menú principal ────────────────────────────────────────────────────────

    public void ShowMenu(ManagementSystem managementSystem)

    {

        while (true)

        {

            AnsiConsole.Write(new Rule($"[{ColorPrimary}]MAIN MENU[/]").RuleStyle(ColorPrimary));

            AnsiConsole.WriteLine();


            var choice = AnsiConsole.Prompt(

                new SelectionPrompt<string>()

                    .Title($"[{ColorAccent}]Select an operation:[/]")

                    .HighlightStyle(new Style(Color.Cyan1, decoration: Decoration.Bold))

                    .PageSize(10)

                    .AddChoices(

                        "[[ 1 ]]  Add Student",

                        "[[ 2 ]]  Add Course Rating",

                        "[[ 3 ]]  View All Registrations",

                        "[[ 4 ]]  View a Registration",

                        "[[ 5 ]]  Exit"));


            AnsiConsole.WriteLine();

            int option = int.Parse(choice.Substring(3, 1));


            if (option == 5)

            {

                managementSystem.SaveData("students.json");

                AnsiConsole.Write(new Rule($"[{ColorAccent}]SESSION TERMINATED[/]").RuleStyle(ColorAccent));

                AnsiConsole.MarkupLine($"\n[{ColorMuted}]Goodbye, Commander.[/]\n");

                return;

            }


            switch (option)

            {

                case 1: AddStudent(managementSystem);          break;

                case 2: AddCourseRating(managementSystem);     break;

                case 3: ViewAllRegistrations(managementSystem); break;

                case 4: ViewRegistration(managementSystem);    break;

                default:

                    AnsiConsole.MarkupLine($"[{ColorWarning}]Invalid option.[/]");

                    break;

            }


            Pause();

        }

    }


    // ── Agregar estudiante ────────────────────────────────────────────────────

    public void AddStudent(ManagementSystem managementSystem)

    {

        AnsiConsole.Write(new Rule($"[{ColorPrimary}]ADD STUDENT[/]").RuleStyle(ColorPrimary));

        AnsiConsole.WriteLine();


        string name = AnsiConsole.Prompt(

            new TextPrompt<string>($"[{ColorAccent}]Student name:[/]")

                .ValidationErrorMessage($"[{ColorDanger}]Name cannot be empty.[/]")

                .Validate(v => !string.IsNullOrWhiteSpace(v)));


        var student = new Student(name);

        managementSystem.AddStudent(student);


        AnsiConsole.WriteLine();

        AnsiConsole.Write(

            new Panel($"[{ColorSuccess}]Student [white]{Markup.Escape(name)}[/] added![/]\n[{ColorMuted}]ID: {student.Id}[/]")

                .BorderColor(Color.Green1)

                .Padding(1, 0));

    }


    // ── Agregar calificación ──────────────────────────────────────────────────

    public void AddCourseRating(ManagementSystem managementSystem)

    {

        AnsiConsole.Write(new Rule($"[{ColorPrimary}]ADD COURSE RATING[/]").RuleStyle(ColorPrimary));

        AnsiConsole.WriteLine();


        var studentId = SelectStudent(managementSystem);

        if (studentId == Guid.Empty) return;


        string courseName = AnsiConsole.Prompt(

            new TextPrompt<string>($"[{ColorAccent}]Course name:[/]")

                .ValidationErrorMessage($"[{ColorDanger}]Course cannot be empty.[/]")

                .Validate(v => !string.IsNullOrWhiteSpace(v)));


        double ratingValue = AnsiConsole.Prompt(

            new TextPrompt<double>($"[{ColorAccent}]Rating [[0.0 – 5.0]]:[/]")

                .ValidationErrorMessage($"[{ColorDanger}]Enter a number between 0 and 5.[/]")

                .Validate(v => v >= 0 && v <= 5));


        var rating = new Rating(courseName, ratingValue);

        managementSystem.AddRating(studentId, courseName, rating);


        AnsiConsole.WriteLine();

        AnsiConsole.Write(

            new Panel(

                $"[{ColorSuccess}]Rating [white]{ratingValue:F1}[/] added to course [white]{Markup.Escape(courseName)}[/][/]\n" +

                $"[{ColorMuted}]{RatingBar(ratingValue)}[/]")

                .BorderColor(Color.Green1)

                .Padding(1, 0));

    }


    // ── Ver todos los registros ───────────────────────────────────────────────

    public void ViewAllRegistrations(ManagementSystem managementSystem)

    {

        AnsiConsole.Write(new Rule($"[{ColorPrimary}]ALL REGISTRATIONS[/]").RuleStyle(ColorPrimary));

        AnsiConsole.WriteLine();


        var students = managementSystem.GetAllRegistration();

        if (students.Count == 0)

        {

            AnsiConsole.Write(

                new Panel($"[{ColorWarning}]No students found.[/]")

                    .BorderColor(Color.Yellow1).Padding(1, 0));

            return;

        }


        var table = new Table()

            .Border(TableBorder.Rounded)

            .BorderColor(Color.Cyan1)

            .Caption($"[{ColorMuted}]Total: {students.Count} student(s)[/]")

            .Expand();


        table.AddColumn(new TableColumn($"[bold {ColorAccent}]NAME[/]").LeftAligned());

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]COURSES[/]").LeftAligned());

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]AVERAGE[/]").Centered());

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]PERFORMANCE[/]").Centered().Width(24));


        foreach (var student in students)

        {

            string courses  = string.Join("\n", student.GetCourseRatings().Keys.Select(k => $"• {k}"));

            double avg      = student.AverageRating;

            string avgLabel = avg > 0 ? avg.ToString("F2") : "N/A";

            string bar      = avg > 0 ? $"[{RatingColor(avg)}]{RatingBar(avg)}[/]" : $"[{ColorMuted}]—[/]";

            string avgMarkup = avg > 0

                ? $"[bold {RatingColor(avg)}]{avgLabel}[/]"

                : $"[{ColorMuted}]N/A[/]";


            table.AddRow(

                $"[white]{Markup.Escape(student.Name)}[/]",

                $"[{ColorMuted}]{Markup.Escape(courses)}[/]",

                avgMarkup,

                bar);

        }


        AnsiConsole.Write(table);

    }


    // ── Ver registro individual ───────────────────────────────────────────────

    public void ViewRegistration(ManagementSystem managementSystem)

    {

        AnsiConsole.Write(new Rule($"[{ColorPrimary}]STUDENT DETAIL[/]").RuleStyle(ColorPrimary));

        AnsiConsole.WriteLine();


        var studentId = SelectStudent(managementSystem);

        if (studentId == Guid.Empty) return;


        var student = managementSystem.GetRegistration(studentId);

        if (student == null)

        {

            AnsiConsole.MarkupLine($"[{ColorWarning}]Student not found.[/]");

            return;

        }


        double avg = student.AverageRating;


        // ── Panel de resumen ──

        var summary = new Panel(

            $"[bold white]{Markup.Escape(student.Name)}[/]\n" +

            $"[{ColorMuted}]ID: {student.Id}[/]\n" +

            $"[{ColorMuted}]Courses: {student.GetCourseRatings().Count}[/]\n" +

            $"Average: [{RatingColor(avg)}]{avg:F2}[/]  [{RatingColor(avg)}]{RatingBar(avg)}[/]")

            .Header($"[bold {ColorPrimary}] PROFILE [/]")

            .BorderColor(Color.Cyan1)

            .Padding(1, 0);


        AnsiConsole.Write(summary);

        AnsiConsole.WriteLine();


        // ── Tabla de cursos ──

        var table = new Table()

            .Border(TableBorder.Rounded)

            .BorderColor(Color.Cyan1)

            .Title($"[bold {ColorAccent}]COURSE RATINGS[/]")

            .Caption($"[{ColorMuted}]{student.GetCourseRatings().Count} course(s)[/]");


        table.AddColumn(new TableColumn($"[bold {ColorAccent}]COURSE[/]").LeftAligned());

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]SCORE[/]").Centered().Width(8));

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]BAR[/]").LeftAligned().Width(22));

        table.AddColumn(new TableColumn($"[bold {ColorAccent}]GRADE[/]").Centered().Width(10));


        foreach (var (courseName, rating) in student.GetCourseRatings())

        {

            double score      = rating.RatingValue;

            string colorScore = RatingColor(score);

            string grade      = ScoreToGrade(score);


            table.AddRow(

                $"[white]{Markup.Escape(courseName)}[/]",

                $"[bold {colorScore}]{score:F1}[/]",

                $"[{colorScore}]{RatingBar(score)}[/]",

                $"[bold {colorScore}]{grade}[/]");

        }


        AnsiConsole.Write(table);

    }


    private Guid SelectStudent(ManagementSystem managementSystem)

    {

        var students = managementSystem.GetAllRegistration();

        if (students.Count == 0)

        {

            AnsiConsole.Write(

                new Panel($"[{ColorWarning}]No students available. Add one first.[/]")

                    .BorderColor(Color.Yellow1).Padding(1, 0));

            return Guid.Empty;

        }


        var selection = AnsiConsole.Prompt(

            new SelectionPrompt<string>()

                .Title($"[{ColorAccent}]Select a student:[/]")

                .HighlightStyle(new Style(Color.Cyan1, decoration: Decoration.Bold))

                .PageSize(12)

                .AddChoices(students.Select(s =>

                {

                    double avg   = s.AverageRating;

                    string badge = avg > 0 ? $"[{RatingColor(avg)}]{avg:F1}★[/]" : $"[{ColorMuted}]—[/]";

                    return $"{s.Id} | {badge} [white]{Markup.Escape(s.Name)}[/]";

                })));

        return Guid.Parse(selection.Split(" | ")[0]);

    }


    private void Pause()

    {

        AnsiConsole.WriteLine();

        AnsiConsole.MarkupLine($"[{ColorMuted}]Press [white]ENTER[/] to return to the main menu...[/]");

        Console.ReadLine();

        AnsiConsole.Clear();

        ShowBanner();

    }


    private static string RatingColor(double score) => score switch

    {

        >= 4.5 => "green1",

        >= 4.0 => "green3",

        >= 3.5 => "yellow1",

        >= 3.0 => "orange1",

        _      => "red1"

    };

    

    private static string RatingBar(double score)

    {

        int totalBlocks = 10;

        int filled = (int)Math.Round((score / 5.0) * totalBlocks);


        // Limitar entre 0 y totalBlocks

        filled = Math.Max(0, Math.Min(totalBlocks, filled));


        int empty = totalBlocks - filled;


        return new string('█', filled) + new string('░', empty);

    }



    private static string ScoreToGrade(double score) => score switch

    {

        >= 4.7 => "A+",

        >= 4.3 => "A",

        >= 4.0 => "A-",

        >= 3.7 => "B+",

        >= 3.3 => "B",

        >= 3.0 => "B-",

        >= 2.7 => "C+",

        >= 2.3 => "C",

        _      => "F"

    };

}

```