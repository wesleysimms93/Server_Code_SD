using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text.Json;
using System.Windows.Forms;

namespace PathEditor
{
    public partial class MainForm : Form
    {
        private List<CapturePoint> pathPoints = new List<CapturePoint>();
        private CapturePoint selectedPoint = null;

        public MainForm()
        {
            InitializeComponent();
            this.DoubleBuffered = true;
        }

        private void MainForm_Paint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            foreach (var point in pathPoints)
            {
                point.Draw(g);
            }
        }

        private void MainForm_MouseDown(object sender, MouseEventArgs e)
        {
            foreach (var point in pathPoints)
            {
                if (point.Contains(e.Location))
                {
                    selectedPoint = point;
                    if (e.Button == MouseButtons.Left)
                    {
                        ShowPropertyEditor(selectedPoint);
                    }
                    return;
                }
            }
        }

        private void MainForm_MouseMove(object sender, MouseEventArgs e)
        {
            if (selectedPoint != null && e.Button == MouseButtons.Right)
            {
                selectedPoint.Position = e.Location;
                Invalidate();
            }
        }

        private void MainForm_MouseUp(object sender, MouseEventArgs e)
        {
            selectedPoint = null;
        }

        private void ShowPropertyEditor(CapturePoint point)
        {
            using (PropertyEditor editor = new PropertyEditor(point))
            {
                editor.ShowDialog();
                Invalidate();
            }
        }

        private void LoadPath(string filePath)
        {
            string json = File.ReadAllText(filePath);
            var data = JsonSerializer.Deserialize<PathData>(json);
            pathPoints.Clear();

            foreach (var p in data.Path)
            {
                pathPoints.Add(new CapturePoint(new PointF(p.X, p.Y), p.CaptureType));
            }

            Invalidate();
        }

        private void SavePath(string filePath)
        {
            var data = new PathData();
            foreach (var point in pathPoints)
            {
                data.Path.Add(new PathPoint(point.Position.X, point.Position.Y, point.CaptureType));
            }

            string json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText(filePath, json);
        }

        private void OpenFile_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog { Filter = "JSON Files (*.json)|*.json" };
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                LoadPath(openFileDialog.FileName);
            }
        }

        private void SaveFile_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog { Filter = "JSON Files (*.json)|*.json" };
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                SavePath(saveFileDialog.FileName);
            }
        }
    }

    public class CapturePoint
    {
        public PointF Position { get; set; }
        public string CaptureType { get; set; }
        private static readonly int SIZE = 10;

        public CapturePoint(PointF position, string captureType)
        {
            Position = position;
            CaptureType = captureType;
        }

        public void Draw(Graphics g)
        {
            Brush brush = new SolidBrush(Color.Red);
            g.FillEllipse(brush, Position.X - SIZE / 2, Position.Y - SIZE / 2, SIZE, SIZE);
        }

        public bool Contains(PointF point)
        {
            return (Math.Abs(point.X - Position.X) < SIZE / 2) && (Math.Abs(point.Y - Position.Y) < SIZE / 2);
        }
    }

    public class PropertyEditor : Form
    {
        private CapturePoint capturePoint;
        private ComboBox dropdown;
        private Button saveButton;

        public PropertyEditor(CapturePoint point)
        {
            this.capturePoint = point;
            this.Text = "Edit Capture Point";
            this.Size = new Size(200, 100);

            dropdown = new ComboBox { Left = 10, Top = 10, Width = 150 };
            dropdown.Items.AddRange(new string[] { "Default", "Image Scan", "Video Capture", "Depth Scan" });
            dropdown.SelectedItem = capturePoint.CaptureType;

            saveButton = new Button { Text = "Save", Left = 10, Top = 40 };
            saveButton.Click += SaveCaptureType;

            Controls.Add(dropdown);
            Controls.Add(saveButton);
        }

        private void SaveCaptureType(object sender, EventArgs e)
        {
            capturePoint.CaptureType = dropdown.SelectedItem.ToString();
            this.Close();
        }
    }

    public class PathData
    {
        public List<PathPoint> Path { get; set; } = new List<PathPoint>();
    }

    public class PathPoint
    {-
        public float X { get; set; }
        public float Y { get; set; }
        public string CaptureType { get; set; }

        public PathPoint(float x, float y, string captureType)
        {
            X = x;
            Y = y;
            CaptureType = captureType;
        }
    }
}
