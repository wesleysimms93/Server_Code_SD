namespace UserPathingCreatorTest
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            Panel panelMenu;
            load_file_button = new Button();
            save_button = new Button();
            new_file_button = new Button();
            label1 = new Label();
            panel1 = new Panel();
            label2 = new Label();
            backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            pathingCanvas = new Panel();
            openFileDialog1 = new OpenFileDialog();
            bindingSource1 = new BindingSource(components);
            panelMenu = new Panel();
            panelMenu.SuspendLayout();
            panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)bindingSource1).BeginInit();
            SuspendLayout();
            // 
            // panelMenu
            // 
            panelMenu.BackColor = Color.ForestGreen;
            panelMenu.Controls.Add(load_file_button);
            panelMenu.Controls.Add(save_button);
            panelMenu.Controls.Add(new_file_button);
            panelMenu.Controls.Add(label1);
            panelMenu.Dock = DockStyle.Left;
            panelMenu.Location = new Point(0, 0);
            panelMenu.Margin = new Padding(2, 4, 2, 4);
            panelMenu.Name = "panelMenu";
            panelMenu.Size = new Size(500, 1048);
            panelMenu.TabIndex = 1;
            // 
            // load_file_button
            // 
            load_file_button.Location = new Point(102, 261);
            load_file_button.Margin = new Padding(2, 4, 2, 4);
            load_file_button.Name = "load_file_button";
            load_file_button.Size = new Size(339, 69);
            load_file_button.TabIndex = 6;
            load_file_button.Text = "⮹ Load File";
            load_file_button.UseVisualStyleBackColor = true;
            load_file_button.Click += button1_Click_2;
            // 
            // save_button
            // 
            save_button.Location = new Point(161, 883);
            save_button.Margin = new Padding(2, 4, 2, 4);
            save_button.Name = "save_button";
            save_button.Size = new Size(182, 99);
            save_button.TabIndex = 4;
            save_button.Text = "Save File";
            save_button.UseVisualStyleBackColor = true;
            save_button.Click += button4_Click;
            // 
            // new_file_button
            // 
            new_file_button.Location = new Point(102, 120);
            new_file_button.Margin = new Padding(2, 4, 2, 4);
            new_file_button.Name = "new_file_button";
            new_file_button.Size = new Size(339, 69);
            new_file_button.TabIndex = 1;
            new_file_button.Text = " ✏️ New File";
            new_file_button.UseVisualStyleBackColor = true;
            new_file_button.Click += button1_Click_1;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Lucida Console", 8.5F);
            label1.ForeColor = Color.White;
            label1.Location = new Point(48, 28);
            label1.Margin = new Padding(2, 0, 2, 0);
            label1.Name = "label1";
            label1.Size = new Size(399, 29);
            label1.TabIndex = 0;
            label1.Text = "🛠️ User Pathing Creator";
            // 
            // panel1
            // 
            panel1.BackColor = Color.Khaki;
            panel1.Controls.Add(label2);
            panel1.Dock = DockStyle.Top;
            panel1.ForeColor = Color.ForestGreen;
            panel1.Location = new Point(500, 0);
            panel1.Margin = new Padding(2, 4, 2, 4);
            panel1.Name = "panel1";
            panel1.Size = new Size(1884, 111);
            panel1.TabIndex = 2;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Arial", 14.1F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label2.Location = new Point(35, 28);
            label2.Margin = new Padding(2, 0, 2, 0);
            label2.Name = "label2";
            label2.Size = new Size(320, 53);
            label2.TabIndex = 0;
            label2.Text = "DASHBOARD";
            // 
            // pathingCanvas
            // 
            pathingCanvas.Location = new Point(525, 261);
            pathingCanvas.Name = "pathingCanvas";
            pathingCanvas.Size = new Size(1825, 630);
            pathingCanvas.TabIndex = 3;
            // 
            // openFileDialog1
            // 
            openFileDialog1.FileName = "openFileDialog1";
            openFileDialog1.FileOk += openFileDialog1_FileOk;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(23F, 45F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.Beige;
            ClientSize = new Size(2384, 1048);
            Controls.Add(pathingCanvas);
            Controls.Add(panel1);
            Controls.Add(panelMenu);
            Font = new Font("Arial", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            ForeColor = Color.ForestGreen;
            Margin = new Padding(4);
            Name = "Form1";
            Text = "🛠️ User Pathing Creator";
            Load += Form1_Load;
            panelMenu.ResumeLayout(false);
            panelMenu.PerformLayout();
            panel1.ResumeLayout(false);
            panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)bindingSource1).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private Label label1;
        private Panel panel1;
        private Label label2;
        private Button new_file_button;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private Button save_button;
        private Button load_file_button;
        private Panel pathingCanvas;
        private OpenFileDialog openFileDialog1;
        private BindingSource bindingSource1;
    }
}
