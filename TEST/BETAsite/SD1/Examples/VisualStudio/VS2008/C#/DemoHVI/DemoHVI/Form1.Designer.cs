namespace DemoHVI
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
            this.readValueLabel = new System.Windows.Forms.Label();
            this.value2writeLabel = new System.Windows.Forms.Label();
            this.value2write = new System.Windows.Forms.NumericUpDown();
            this.readValue = new System.Windows.Forms.TextBox();
            this.writeButton = new System.Windows.Forms.Button();
            this.readButton = new System.Windows.Forms.Button();
            this.HVIpath = new System.Windows.Forms.TextBox();
            this.HVIlabel = new System.Windows.Forms.Label();
            this.HVIbutton = new System.Windows.Forms.Button();
            this.moduleLabel = new System.Windows.Forms.Label();
            this.moduleName = new System.Windows.Forms.TextBox();
            this.registerGroupBox = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.registerNumber = new System.Windows.Forms.NumericUpDown();
            this.openButton = new System.Windows.Forms.Button();
            this.startButton = new System.Windows.Forms.Button();
            this.stopButton = new System.Windows.Forms.Button();
            this.pauseButton = new System.Windows.Forms.Button();
            this.resumeButton = new System.Windows.Forms.Button();
            this.triggerGroupBox = new System.Windows.Forms.GroupBox();
            this.label2 = new System.Windows.Forms.Label();
            this.triggerNumber = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.trigger2write = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.readTrigger = new System.Windows.Forms.TextBox();
            this.triggerWrite = new System.Windows.Forms.Button();
            this.triggerRead = new System.Windows.Forms.Button();
            this.closeButton = new System.Windows.Forms.Button();
            this.moduleButton = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.value2write)).BeginInit();
            this.registerGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.registerNumber)).BeginInit();
            this.triggerGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.triggerNumber)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trigger2write)).BeginInit();
            this.SuspendLayout();
            // 
            // readValueLabel
            // 
            this.readValueLabel.AutoSize = true;
            this.readValueLabel.Location = new System.Drawing.Point(6, 79);
            this.readValueLabel.Name = "readValueLabel";
            this.readValueLabel.Size = new System.Drawing.Size(65, 13);
            this.readValueLabel.TabIndex = 5;
            this.readValueLabel.Text = "Read value:";
            // 
            // value2writeLabel
            // 
            this.value2writeLabel.AutoSize = true;
            this.value2writeLabel.Location = new System.Drawing.Point(6, 43);
            this.value2writeLabel.Name = "value2writeLabel";
            this.value2writeLabel.Size = new System.Drawing.Size(74, 13);
            this.value2writeLabel.TabIndex = 4;
            this.value2writeLabel.Text = "Value to write:";
            // 
            // value2write
            // 
            this.value2write.Location = new System.Drawing.Point(86, 41);
            this.value2write.Maximum = new decimal(new int[] {
            -1,
            0,
            0,
            0});
            this.value2write.Name = "value2write";
            this.value2write.Size = new System.Drawing.Size(89, 20);
            this.value2write.TabIndex = 3;
            this.value2write.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // readValue
            // 
            this.readValue.Location = new System.Drawing.Point(77, 76);
            this.readValue.Name = "readValue";
            this.readValue.ReadOnly = true;
            this.readValue.Size = new System.Drawing.Size(98, 20);
            this.readValue.TabIndex = 6;
            this.readValue.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // writeButton
            // 
            this.writeButton.Enabled = false;
            this.writeButton.Location = new System.Drawing.Point(180, 40);
            this.writeButton.Name = "writeButton";
            this.writeButton.Size = new System.Drawing.Size(75, 23);
            this.writeButton.TabIndex = 7;
            this.writeButton.Text = "Write";
            this.writeButton.UseVisualStyleBackColor = true;
            this.writeButton.Click += new System.EventHandler(this.writeButton_Click);
            // 
            // readButton
            // 
            this.readButton.Enabled = false;
            this.readButton.Location = new System.Drawing.Point(181, 74);
            this.readButton.Name = "readButton";
            this.readButton.Size = new System.Drawing.Size(75, 23);
            this.readButton.TabIndex = 8;
            this.readButton.Text = "Read";
            this.readButton.UseVisualStyleBackColor = true;
            this.readButton.Click += new System.EventHandler(this.readButton_Click);
            // 
            // HVIpath
            // 
            this.HVIpath.Location = new System.Drawing.Point(47, 12);
            this.HVIpath.Name = "HVIpath";
            this.HVIpath.ReadOnly = true;
            this.HVIpath.Size = new System.Drawing.Size(144, 20);
            this.HVIpath.TabIndex = 9;
            this.HVIpath.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // HVIlabel
            // 
            this.HVIlabel.AutoSize = true;
            this.HVIlabel.Location = new System.Drawing.Point(13, 15);
            this.HVIlabel.Name = "HVIlabel";
            this.HVIlabel.Size = new System.Drawing.Size(28, 13);
            this.HVIlabel.TabIndex = 10;
            this.HVIlabel.Text = "HVI:";
            // 
            // HVIbutton
            // 
            this.HVIbutton.Location = new System.Drawing.Point(197, 9);
            this.HVIbutton.Name = "HVIbutton";
            this.HVIbutton.Size = new System.Drawing.Size(75, 23);
            this.HVIbutton.TabIndex = 11;
            this.HVIbutton.Text = "Browse";
            this.HVIbutton.UseVisualStyleBackColor = true;
            this.HVIbutton.Click += new System.EventHandler(this.HVIbutton_Click);
            // 
            // moduleLabel
            // 
            this.moduleLabel.AutoSize = true;
            this.moduleLabel.Location = new System.Drawing.Point(15, 102);
            this.moduleLabel.Name = "moduleLabel";
            this.moduleLabel.Size = new System.Drawing.Size(76, 13);
            this.moduleLabel.TabIndex = 13;
            this.moduleLabel.Text = "Module Name:";
            // 
            // moduleName
            // 
            this.moduleName.Location = new System.Drawing.Point(97, 99);
            this.moduleName.Name = "moduleName";
            this.moduleName.Size = new System.Drawing.Size(124, 20);
            this.moduleName.TabIndex = 12;
            this.moduleName.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.moduleName.TextChanged += new System.EventHandler(this.moduleName_TextChanged);
            // 
            // registerGroupBox
            // 
            this.registerGroupBox.Controls.Add(this.label1);
            this.registerGroupBox.Controls.Add(this.registerNumber);
            this.registerGroupBox.Controls.Add(this.value2writeLabel);
            this.registerGroupBox.Controls.Add(this.value2write);
            this.registerGroupBox.Controls.Add(this.readValueLabel);
            this.registerGroupBox.Controls.Add(this.readValue);
            this.registerGroupBox.Controls.Add(this.writeButton);
            this.registerGroupBox.Controls.Add(this.readButton);
            this.registerGroupBox.Location = new System.Drawing.Point(11, 125);
            this.registerGroupBox.Name = "registerGroupBox";
            this.registerGroupBox.Size = new System.Drawing.Size(261, 105);
            this.registerGroupBox.TabIndex = 14;
            this.registerGroupBox.TabStop = false;
            this.registerGroupBox.Text = "Register";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(6, 16);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(47, 13);
            this.label1.TabIndex = 10;
            this.label1.Text = "Number:";
            // 
            // registerNumber
            // 
            this.registerNumber.Location = new System.Drawing.Point(59, 14);
            this.registerNumber.Maximum = new decimal(new int[] {
            15,
            0,
            0,
            0});
            this.registerNumber.Name = "registerNumber";
            this.registerNumber.Size = new System.Drawing.Size(196, 20);
            this.registerNumber.TabIndex = 9;
            this.registerNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // openButton
            // 
            this.openButton.Location = new System.Drawing.Point(12, 38);
            this.openButton.Name = "openButton";
            this.openButton.Size = new System.Drawing.Size(75, 23);
            this.openButton.TabIndex = 15;
            this.openButton.Text = "Open";
            this.openButton.UseVisualStyleBackColor = true;
            this.openButton.Click += new System.EventHandler(this.openButton_Click);
            // 
            // startButton
            // 
            this.startButton.Enabled = false;
            this.startButton.Location = new System.Drawing.Point(197, 38);
            this.startButton.Name = "startButton";
            this.startButton.Size = new System.Drawing.Size(75, 23);
            this.startButton.TabIndex = 16;
            this.startButton.Text = "Start";
            this.startButton.UseVisualStyleBackColor = true;
            this.startButton.Click += new System.EventHandler(this.startButton_Click);
            // 
            // stopButton
            // 
            this.stopButton.Enabled = false;
            this.stopButton.Location = new System.Drawing.Point(11, 67);
            this.stopButton.Name = "stopButton";
            this.stopButton.Size = new System.Drawing.Size(75, 23);
            this.stopButton.TabIndex = 17;
            this.stopButton.Text = "Stop";
            this.stopButton.UseVisualStyleBackColor = true;
            this.stopButton.Click += new System.EventHandler(this.stopButton_Click);
            // 
            // pauseButton
            // 
            this.pauseButton.Enabled = false;
            this.pauseButton.Location = new System.Drawing.Point(104, 67);
            this.pauseButton.Name = "pauseButton";
            this.pauseButton.Size = new System.Drawing.Size(75, 23);
            this.pauseButton.TabIndex = 18;
            this.pauseButton.Text = "Pause";
            this.pauseButton.UseVisualStyleBackColor = true;
            this.pauseButton.Click += new System.EventHandler(this.pauseButton_Click);
            // 
            // resumeButton
            // 
            this.resumeButton.Enabled = false;
            this.resumeButton.Location = new System.Drawing.Point(197, 67);
            this.resumeButton.Name = "resumeButton";
            this.resumeButton.Size = new System.Drawing.Size(75, 23);
            this.resumeButton.TabIndex = 19;
            this.resumeButton.Text = "Resume";
            this.resumeButton.UseVisualStyleBackColor = true;
            this.resumeButton.Click += new System.EventHandler(this.resumeButton_Click);
            // 
            // triggerGroupBox
            // 
            this.triggerGroupBox.Controls.Add(this.label2);
            this.triggerGroupBox.Controls.Add(this.triggerNumber);
            this.triggerGroupBox.Controls.Add(this.label3);
            this.triggerGroupBox.Controls.Add(this.trigger2write);
            this.triggerGroupBox.Controls.Add(this.label4);
            this.triggerGroupBox.Controls.Add(this.readTrigger);
            this.triggerGroupBox.Controls.Add(this.triggerWrite);
            this.triggerGroupBox.Controls.Add(this.triggerRead);
            this.triggerGroupBox.Location = new System.Drawing.Point(11, 236);
            this.triggerGroupBox.Name = "triggerGroupBox";
            this.triggerGroupBox.Size = new System.Drawing.Size(261, 105);
            this.triggerGroupBox.TabIndex = 20;
            this.triggerGroupBox.TabStop = false;
            this.triggerGroupBox.Text = "PXI trigger";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(6, 16);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(47, 13);
            this.label2.TabIndex = 10;
            this.label2.Text = "Number:";
            // 
            // triggerNumber
            // 
            this.triggerNumber.Location = new System.Drawing.Point(59, 14);
            this.triggerNumber.Maximum = new decimal(new int[] {
            7,
            0,
            0,
            0});
            this.triggerNumber.Name = "triggerNumber";
            this.triggerNumber.Size = new System.Drawing.Size(196, 20);
            this.triggerNumber.TabIndex = 9;
            this.triggerNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(6, 43);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(74, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "Value to write:";
            // 
            // trigger2write
            // 
            this.trigger2write.Location = new System.Drawing.Point(86, 41);
            this.trigger2write.Maximum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.trigger2write.Name = "trigger2write";
            this.trigger2write.Size = new System.Drawing.Size(89, 20);
            this.trigger2write.TabIndex = 3;
            this.trigger2write.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(6, 79);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(65, 13);
            this.label4.TabIndex = 5;
            this.label4.Text = "Read value:";
            // 
            // readTrigger
            // 
            this.readTrigger.Location = new System.Drawing.Point(77, 76);
            this.readTrigger.Name = "readTrigger";
            this.readTrigger.ReadOnly = true;
            this.readTrigger.Size = new System.Drawing.Size(98, 20);
            this.readTrigger.TabIndex = 6;
            this.readTrigger.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // triggerWrite
            // 
            this.triggerWrite.Enabled = false;
            this.triggerWrite.Location = new System.Drawing.Point(181, 38);
            this.triggerWrite.Name = "triggerWrite";
            this.triggerWrite.Size = new System.Drawing.Size(75, 23);
            this.triggerWrite.TabIndex = 7;
            this.triggerWrite.Text = "Write";
            this.triggerWrite.UseVisualStyleBackColor = true;
            this.triggerWrite.Click += new System.EventHandler(this.triggerWrite_Click);
            // 
            // triggerRead
            // 
            this.triggerRead.Enabled = false;
            this.triggerRead.Location = new System.Drawing.Point(181, 74);
            this.triggerRead.Name = "triggerRead";
            this.triggerRead.Size = new System.Drawing.Size(75, 23);
            this.triggerRead.TabIndex = 8;
            this.triggerRead.Text = "Read";
            this.triggerRead.UseVisualStyleBackColor = true;
            this.triggerRead.Click += new System.EventHandler(this.triggerRead_Click);
            // 
            // closeButton
            // 
            this.closeButton.Enabled = false;
            this.closeButton.Location = new System.Drawing.Point(104, 38);
            this.closeButton.Name = "closeButton";
            this.closeButton.Size = new System.Drawing.Size(75, 23);
            this.closeButton.TabIndex = 21;
            this.closeButton.Text = "Close";
            this.closeButton.UseVisualStyleBackColor = true;
            this.closeButton.Click += new System.EventHandler(this.closeButton_Click);
            // 
            // moduleButton
            // 
            this.moduleButton.Enabled = false;
            this.moduleButton.Location = new System.Drawing.Point(227, 97);
            this.moduleButton.Name = "moduleButton";
            this.moduleButton.Size = new System.Drawing.Size(45, 23);
            this.moduleButton.TabIndex = 22;
            this.moduleButton.Text = "Get";
            this.moduleButton.UseVisualStyleBackColor = true;
            this.moduleButton.Click += new System.EventHandler(this.moduleButton_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(280, 350);
            this.Controls.Add(this.moduleButton);
            this.Controls.Add(this.closeButton);
            this.Controls.Add(this.triggerGroupBox);
            this.Controls.Add(this.resumeButton);
            this.Controls.Add(this.pauseButton);
            this.Controls.Add(this.stopButton);
            this.Controls.Add(this.startButton);
            this.Controls.Add(this.openButton);
            this.Controls.Add(this.registerGroupBox);
            this.Controls.Add(this.moduleLabel);
            this.Controls.Add(this.moduleName);
            this.Controls.Add(this.HVIbutton);
            this.Controls.Add(this.HVIlabel);
            this.Controls.Add(this.HVIpath);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.value2write)).EndInit();
            this.registerGroupBox.ResumeLayout(false);
            this.registerGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.registerNumber)).EndInit();
            this.triggerGroupBox.ResumeLayout(false);
            this.triggerGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.triggerNumber)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trigger2write)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label readValueLabel;
        private System.Windows.Forms.Label value2writeLabel;
        private System.Windows.Forms.NumericUpDown value2write;
        private System.Windows.Forms.TextBox readValue;
        private System.Windows.Forms.Button writeButton;
        private System.Windows.Forms.Button readButton;
        private System.Windows.Forms.TextBox HVIpath;
        private System.Windows.Forms.Label HVIlabel;
        private System.Windows.Forms.Button HVIbutton;
        private System.Windows.Forms.Label moduleLabel;
        private System.Windows.Forms.TextBox moduleName;
        private System.Windows.Forms.GroupBox registerGroupBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown registerNumber;
        private System.Windows.Forms.Button openButton;
        private System.Windows.Forms.Button startButton;
        private System.Windows.Forms.Button stopButton;
        private System.Windows.Forms.Button pauseButton;
        private System.Windows.Forms.Button resumeButton;
        private System.Windows.Forms.GroupBox triggerGroupBox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.NumericUpDown triggerNumber;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown trigger2write;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox readTrigger;
        private System.Windows.Forms.Button triggerWrite;
        private System.Windows.Forms.Button triggerRead;
        private System.Windows.Forms.Button closeButton;
        private System.Windows.Forms.Button moduleButton;
    }
}

