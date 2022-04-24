namespace FSXControl
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.start = new System.Windows.Forms.Button();
            this.bStop = new System.Windows.Forms.Button();
            this.file_label = new System.Windows.Forms.Label();
            this.listBox1 = new System.Windows.Forms.ListBox();
            this.lbl_loaded = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // start
            // 
            this.start.Location = new System.Drawing.Point(12, 167);
            this.start.Margin = new System.Windows.Forms.Padding(4);
            this.start.Name = "start";
            this.start.Size = new System.Drawing.Size(156, 37);
            this.start.TabIndex = 7;
            this.start.Text = "Start";
            this.start.UseVisualStyleBackColor = true;
            this.start.Click += new System.EventHandler(this.buttonStart);
            // 
            // bStop
            // 
            this.bStop.Location = new System.Drawing.Point(176, 167);
            this.bStop.Margin = new System.Windows.Forms.Padding(4);
            this.bStop.Name = "bStop";
            this.bStop.Size = new System.Drawing.Size(156, 37);
            this.bStop.TabIndex = 8;
            this.bStop.Text = "Stop";
            this.bStop.UseVisualStyleBackColor = true;
            this.bStop.Click += new System.EventHandler(this.buttonStop_Click);
            // 
            // file_label
            // 
            this.file_label.Location = new System.Drawing.Point(13, 9);
            this.file_label.Name = "file_label";
            this.file_label.Size = new System.Drawing.Size(91, 26);
            this.file_label.TabIndex = 10;
            this.file_label.Text = "Files";
            // 
            // listBox1
            // 
            this.listBox1.FormattingEnabled = true;
            this.listBox1.ItemHeight = 16;
            this.listBox1.Location = new System.Drawing.Point(12, 43);
            this.listBox1.Name = "listBox1";
            this.listBox1.Size = new System.Drawing.Size(320, 84);
            this.listBox1.TabIndex = 12;
            this.listBox1.SelectedIndexChanged += new System.EventHandler(this.listBox1_SelectedIndexChanged);
            // 
            // lbl_loaded
            // 
            this.lbl_loaded.Location = new System.Drawing.Point(138, 130);
            this.lbl_loaded.Name = "lbl_loaded";
            this.lbl_loaded.Size = new System.Drawing.Size(73, 14);
            this.lbl_loaded.TabIndex = 13;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(343, 214);
            this.Controls.Add(this.lbl_loaded);
            this.Controls.Add(this.listBox1);
            this.Controls.Add(this.file_label);
            this.Controls.Add(this.bStop);
            this.Controls.Add(this.start);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label lbl_loaded;

        private System.Windows.Forms.ListBox listBox1;

        private System.Windows.Forms.Label file_label;

        private System.Windows.Forms.Button bStop;

        private System.Windows.Forms.Button start;

        #endregion
    }
}