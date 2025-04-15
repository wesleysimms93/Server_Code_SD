using System.Runtime.InteropServices;
using System.IO;
using System.Windows.Forms;
using System.Drawing;
using System.Linq;
using System.Collections.Generic;

namespace UserPathingCreatorTest
{
    public partial class Form1 : Form
    {
        private int borderSize = 2;
        private List<PathPoint> pathPoints = new List<PathPoint>();
        private List<PathPoint> pinnedPoints = new List<PathPoint>();
        private ListBox pinnedListBox = new ListBox();
        private Label coordLabel = new Label();
        private Panel pinnedPanel = new Panel();
        private Button toggleListButton = new Button();

        // Zoom-related variables
        private float zoomLevel = 1.0f;
        private const float zoomStep = 0.1f;
        private const float zoomMin = 0.33f;
        private const float zoomMax = 3.0f;

        public Form1()
        {
            InitializeComponent();

            new_file_button.Click += new_file_button_Click;
            save_button.Click += save_file_button_Click;
            load_file_button.Click += load_file_button_Click;


            // Enable double buffering
            this.DoubleBuffered = true;
            this.SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint | ControlStyles.OptimizedDoubleBuffer, true);
            this.Padding = new Padding(borderSize);
            this.BackColor = Color.FromArgb(127, 207, 120);

            // Coordinate label
            coordLabel.AutoSize = true;
            coordLabel.Font = new Font("Segoe UI", 9);
            coordLabel.ForeColor = Color.Black;
            coordLabel.BackColor = Color.White;
            coordLabel.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            coordLabel.TextAlign = ContentAlignment.TopRight;
            coordLabel.Location = new Point(this.Width - 150, 5);
            this.Controls.Add(coordLabel);

            this.Resize += (s, e) =>
            {
                coordLabel.Location = new Point(this.Width - coordLabel.Width - 20, 5);
                pathingCanvas.Invalidate();
            };

            // Setup pinned panel (always visible)
            pinnedPanel.Width = 200;
            pinnedPanel.Dock = DockStyle.Right;
            pinnedPanel.BackColor = Color.White;
            pinnedPanel.Visible = true;

            // Toggle button
            toggleListButton.Text = "Hide";
            toggleListButton.Height = 60;
            toggleListButton.Dock = DockStyle.Top;
            toggleListButton.FlatStyle = FlatStyle.Flat;
            toggleListButton.BackColor = Color.LightGray;
            toggleListButton.Click += (s, e) =>
            {
                pinnedListBox.Visible = !pinnedListBox.Visible;
                toggleListButton.Text = pinnedListBox.Visible ? "Hide" : "Show";
            };

            // List box setup
            pinnedListBox.Dock = DockStyle.Fill;
            pinnedListBox.Font = new Font("Segoe UI", 4.5f); // Reduced font size
            pinnedListBox.Visible = true;

            // Add to panel
            pinnedPanel.Controls.Add(pinnedListBox);
            pinnedPanel.Controls.Add(toggleListButton);
            this.Controls.Add(pinnedPanel);

            // Canvas setup
            pathingCanvas.Dock = DockStyle.Fill;
            pathingCanvas.BackColor = Color.White;
            pathingCanvas.Paint += PathingCanvas_Paint;
            pathingCanvas.MouseMove += PathingCanvas_MouseMove;
            pathingCanvas.MouseClick += PathingCanvas_MouseClick;
            pathingCanvas.MouseWheel += PathingCanvas_MouseWheel;
            pathingCanvas.Focus(); // ensures it gets scroll events

            // Force double buffering on canvas
            pathingCanvas.GetType().GetProperty("DoubleBuffered",
                System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                ?.SetValue(pathingCanvas, true, null);

            this.Shown += (s, e) => pathingCanvas.Invalidate();
        }

        [DllImport("user32.DLL", EntryPoint = "ReleaseCapture")]
        private extern static void ReleaseCapture();

        [DllImport("user32.DLL", EntryPoint = "SendMessage")]
        private extern static void SendMessage(System.IntPtr hWnd, int wMsg, int wParam, int lParam);

        private void save_file_button_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog
            {
                Filter = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*",
                Title = "Save Path Points"
            };

            if (sfd.ShowDialog() == DialogResult.OK)
            {
                List<string> lines = new List<string>();

                foreach (var item in pinnedListBox.Items)
                {
                    string[] coords = item.ToString().Split(',');
                    if (coords.Length == 2 &&
                        int.TryParse(coords[0], out int x) &&
                        int.TryParse(coords[1], out int y))
                    {
                        lines.Add($"{x} {y}");
                    }
                }

                File.WriteAllLines(sfd.FileName, lines);
                MessageBox.Show("File saved successfully!");
            }
        }


        private void panelTitleBar_MouseDown(object sender, MouseEventArgs e)
        {
            ReleaseCapture();
            SendMessage(this.Handle, 0x112, 0xf012, 0);
        }

        private void Form1_Load(object sender, EventArgs e) { }
        private void button1_Click(object sender, EventArgs e) { }
        private void button1_Click_1(object sender, EventArgs e) => openFileDialog1.ShowDialog();
        private void button4_Click(object sender, EventArgs e) { }
        private void button1_Click_2(object sender, EventArgs e) { }

        private void new_file_button_Click(object sender, EventArgs e)
        {
            DialogResult result = MessageBox.Show(
                "Create new file?\nThis will clear all current points.",
                "Confirm New File",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question
            );

            if (result == DialogResult.Yes)
            {
                pathPoints.Clear();
                pinnedPoints.Clear();
                pinnedListBox.Items.Clear();
                pathingCanvas.Invalidate();

                MessageBox.Show("New file started. All points cleared.", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }


        private void load_file_button_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog
            {
                Filter = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*",
                Title = "Load Path Points"
            };

            if (ofd.ShowDialog() == DialogResult.OK)
            {
                pathPoints.Clear();
                pinnedPoints.Clear();
                pinnedListBox.Items.Clear();

                string[] lines = File.ReadAllLines(ofd.FileName);
                foreach (string line in lines)
                {
                    string[] parts = line.Trim().Split(' ');
                    if (parts.Length == 2 &&
                        int.TryParse(parts[0], out int x) &&
                        int.TryParse(parts[1], out int y))
                    {
                        PathPoint point = new PathPoint { X = x, Y = y, Action = "Added" };
                        pathPoints.Add(point);
                        pinnedPoints.Add(point);
                        pinnedListBox.Items.Add($"{x},{y}");
                    }
                }

                pathingCanvas.Invalidate();
                MessageBox.Show("File loaded successfully!");
            }
        }


        private void openFileDialog1_FileOk(object sender, System.ComponentModel.CancelEventArgs e) { }

        private void PathingCanvas_Paint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            Control canvas = sender as Control;
            if (canvas == null) return;

            g.Clear(Color.White);

            Pen axisPen = new Pen(Color.Black, 2);
            Pen gridPen = new Pen(Color.LightGray, 1);
            int spacing = (int)(20 * zoomLevel); // Adjust spacing based on zoom

            // Only draw grid in the upper-right quadrant
            for (int x = 0; x <= canvas.Width; x += spacing)
                g.DrawLine(gridPen, x, 0, x, canvas.Height);

            for (int y = 0; y <= canvas.Height; y += spacing)
                g.DrawLine(gridPen, 0, y, canvas.Width, y);

            // Draw axes on the top-left corner of the grid
            g.DrawLine(axisPen, 0, 0, 0, canvas.Height); // Y axis
            g.DrawLine(axisPen, 0, 0, canvas.Width, 0);  // X axis

            int dotSize = (int)(10 * zoomLevel); // Adjust dot size based on zoom
            int centerX = canvas.Width / 2;
            int centerY = canvas.Height / 2;

            foreach (var point in pathPoints)
            {
                int x = centerX + (int)(point.X * zoomLevel);
                int y = centerY - (int)(point.Y * zoomLevel);

                // Check if point is within visible area (+ some buffer for dot size)
                if (x < 0 || x >= canvas.Width || y < 0 || y >= canvas.Height)
                    continue;

                Brush brush = point.Action == "Visible" ? Brushes.Green :
                              point.Action == "IR" ? Brushes.Orange :
                              point.Action == "Added" ? Brushes.Blue :
                              Brushes.Red;

                g.FillEllipse(brush, x - dotSize / 2, y - dotSize / 2, dotSize, dotSize);
            }
        }

        private void PathingCanvas_MouseMove(object sender, MouseEventArgs e)
        {
            int centerX = pathingCanvas.Width / 2;
            int centerY = pathingCanvas.Height / 2;
            bool hovering = false;

            foreach (var point in pathPoints)
            {
                int px = (int)(centerX + point.X * zoomLevel);
                int py = (int)(centerY - point.Y * zoomLevel);

                Rectangle hitbox = new Rectangle(px - 5, py - 5, 10, 10);

                if (hitbox.Contains(e.Location))
                {
                    coordLabel.Text = "(" + point.X.ToString("F5") + ", " + point.Y.ToString("F5") + ")";
                    coordLabel.Location = new Point(this.Width - coordLabel.Width - 20, 5);
                    hovering = true;
                    break;
                }
            }

            if (!hovering)
                coordLabel.Text = string.Empty;
        }

        private void PathingCanvas_MouseClick(object sender, MouseEventArgs e)
        {
            int centerX = pathingCanvas.Width / 2;
            int centerY = pathingCanvas.Height / 2;

            // Convert clicked pixel to logical (x, y) coordinates
            int logicalX = (int)((e.X - centerX) / zoomLevel);
            int logicalY = (int)((centerY - e.Y) / zoomLevel);

            if (e.Button == MouseButtons.Right)
            {
                // Right-click: check for a nearby dot and remove it
                for (int i = 0; i < pathPoints.Count; i++)
                {
                    int px = (int)(centerX + pathPoints[i].X * zoomLevel);
                    int py = (int)(centerY - pathPoints[i].Y * zoomLevel);

                    Rectangle hitbox = new Rectangle(px - 5, py - 5, 10, 10);
                    if (hitbox.Contains(e.Location))
                    {
                        var pointToRemove = pathPoints[i];
                        pathPoints.RemoveAt(i);

                        pinnedPoints.Remove(pointToRemove);
                        pinnedListBox.Items.Remove($"{pointToRemove.X},{pointToRemove.Y}");

                        pathingCanvas.Invalidate();
                        return;
                    }
                }
            }
            else if (e.Button == MouseButtons.Left)
            {
                // Left-click: add new point
                PathPoint newPoint = new PathPoint { X = logicalX, Y = logicalY, Action = "Added" };
                pathPoints.Add(newPoint);
                pinnedPoints.Add(newPoint);
                pinnedListBox.Items.Add($"{newPoint.X},{newPoint.Y}");

                pathingCanvas.Invalidate();
            }
        }

        private void PathingCanvas_MouseWheel(object? sender, MouseEventArgs e)
        {
            if (e.Delta > 0)
                zoomLevel = Math.Min(zoomMax, zoomLevel + zoomStep);
            else if (e.Delta < 0)
                zoomLevel = Math.Max(zoomMin, zoomLevel - zoomStep);

            pathingCanvas.Invalidate();
        }
    }

    public class PathPoint
    {
        public int X { get; set; }
        public int Y { get; set; }
        public string Action { get; set; }
    }
}
