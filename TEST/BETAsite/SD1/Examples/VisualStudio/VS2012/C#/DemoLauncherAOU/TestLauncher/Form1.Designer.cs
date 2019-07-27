namespace TestLauncher
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
            this.buttonTestWaveformTrigger = new System.Windows.Forms.Button();
            this.textBoxOutput = new System.Windows.Forms.TextBox();
            this.buttonContinue = new System.Windows.Forms.Button();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.buttonOpen = new System.Windows.Forms.Button();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.buttonClose = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.numericUpDownSlot = new System.Windows.Forms.NumericUpDown();
            this.label2 = new System.Windows.Forms.Label();
            this.numericUpDownChassis = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.textBoxName = new System.Windows.Forms.TextBox();
            this.groupBoxTests = new System.Windows.Forms.GroupBox();
            this.buttonTestTriggerOutClockOut = new System.Windows.Forms.Button();
            this.buttonTestFrequencyModulation = new System.Windows.Forms.Button();
            this.buttonTestWaveformContinuous = new System.Windows.Forms.Button();
            this.buttonTestAMmodulation = new System.Windows.Forms.Button();
            this.buttonTestMultipleWaveforms = new System.Windows.Forms.Button();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.numericUpDownChannel2 = new System.Windows.Forms.NumericUpDown();
            this.numericUpDownChannel = new System.Windows.Forms.NumericUpDown();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownSlot)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChassis)).BeginInit();
            this.groupBoxTests.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChannel2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChannel)).BeginInit();
            this.SuspendLayout();
            // 
            // buttonTestWaveformTrigger
            // 
            this.buttonTestWaveformTrigger.Location = new System.Drawing.Point(15, 79);
            this.buttonTestWaveformTrigger.Name = "buttonTestWaveformTrigger";
            this.buttonTestWaveformTrigger.Size = new System.Drawing.Size(186, 28);
            this.buttonTestWaveformTrigger.TabIndex = 0;
            this.buttonTestWaveformTrigger.Text = "Run WaveformTrigger Demo";
            this.buttonTestWaveformTrigger.UseVisualStyleBackColor = true;
            this.buttonTestWaveformTrigger.Click += new System.EventHandler(this.buttonTestWaveformTrigger_Click);
            // 
            // textBoxOutput
            // 
            this.textBoxOutput.Location = new System.Drawing.Point(212, 19);
            this.textBoxOutput.Multiline = true;
            this.textBoxOutput.Name = "textBoxOutput";
            this.textBoxOutput.Size = new System.Drawing.Size(551, 283);
            this.textBoxOutput.TabIndex = 1;
            // 
            // buttonContinue
            // 
            this.buttonContinue.Location = new System.Drawing.Point(644, 308);
            this.buttonContinue.Name = "buttonContinue";
            this.buttonContinue.Size = new System.Drawing.Size(119, 29);
            this.buttonContinue.TabIndex = 2;
            this.buttonContinue.Text = "CONTINUE";
            this.buttonContinue.UseVisualStyleBackColor = true;
            this.buttonContinue.Click += new System.EventHandler(this.buttonContinue_Click);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.buttonOpen);
            this.groupBox2.Controls.Add(this.textBoxStatus);
            this.groupBox2.Controls.Add(this.buttonClose);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.numericUpDownSlot);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.numericUpDownChassis);
            this.groupBox2.Controls.Add(this.label4);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.textBoxName);
            this.groupBox2.Location = new System.Drawing.Point(12, 12);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(445, 79);
            this.groupBox2.TabIndex = 9;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Module Control";
            // 
            // buttonOpen
            // 
            this.buttonOpen.Location = new System.Drawing.Point(29, 43);
            this.buttonOpen.Name = "buttonOpen";
            this.buttonOpen.Size = new System.Drawing.Size(80, 23);
            this.buttonOpen.TabIndex = 4;
            this.buttonOpen.Text = "Open";
            this.buttonOpen.UseVisualStyleBackColor = true;
            this.buttonOpen.Click += new System.EventHandler(this.buttonOpen_Click);
            // 
            // textBoxStatus
            // 
            this.textBoxStatus.Location = new System.Drawing.Point(268, 46);
            this.textBoxStatus.Name = "textBoxStatus";
            this.textBoxStatus.Size = new System.Drawing.Size(167, 20);
            this.textBoxStatus.TabIndex = 2;
            this.textBoxStatus.Text = "Module Closed";
            // 
            // buttonClose
            // 
            this.buttonClose.Location = new System.Drawing.Point(129, 43);
            this.buttonClose.Name = "buttonClose";
            this.buttonClose.Size = new System.Drawing.Size(81, 24);
            this.buttonClose.TabIndex = 0;
            this.buttonClose.Text = "Close";
            this.buttonClose.UseVisualStyleBackColor = true;
            this.buttonClose.Click += new System.EventHandler(this.buttonClose_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(7, 22);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(35, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Name";
            // 
            // numericUpDownSlot
            // 
            this.numericUpDownSlot.Location = new System.Drawing.Point(384, 20);
            this.numericUpDownSlot.Name = "numericUpDownSlot";
            this.numericUpDownSlot.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownSlot.TabIndex = 3;
            this.numericUpDownSlot.Value = new decimal(new int[] {
            4,
            0,
            0,
            0});
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(239, 22);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(43, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "Chassis";
            // 
            // numericUpDownChassis
            // 
            this.numericUpDownChassis.Location = new System.Drawing.Point(288, 20);
            this.numericUpDownChassis.Name = "numericUpDownChassis";
            this.numericUpDownChassis.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownChassis.TabIndex = 3;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(219, 49);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(37, 13);
            this.label4.TabIndex = 1;
            this.label4.Text = "Status";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(353, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(25, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "Slot";
            // 
            // textBoxName
            // 
            this.textBoxName.Location = new System.Drawing.Point(56, 19);
            this.textBoxName.Name = "textBoxName";
            this.textBoxName.Size = new System.Drawing.Size(167, 20);
            this.textBoxName.TabIndex = 2;
            this.textBoxName.Text = "SD-PXE-AOU-H0002";
            // 
            // groupBoxTests
            // 
            this.groupBoxTests.Controls.Add(this.buttonContinue);
            this.groupBoxTests.Controls.Add(this.textBoxOutput);
            this.groupBoxTests.Controls.Add(this.buttonTestTriggerOutClockOut);
            this.groupBoxTests.Controls.Add(this.buttonTestFrequencyModulation);
            this.groupBoxTests.Controls.Add(this.buttonTestWaveformContinuous);
            this.groupBoxTests.Controls.Add(this.buttonTestAMmodulation);
            this.groupBoxTests.Controls.Add(this.buttonTestMultipleWaveforms);
            this.groupBoxTests.Controls.Add(this.buttonTestWaveformTrigger);
            this.groupBoxTests.Controls.Add(this.label6);
            this.groupBoxTests.Controls.Add(this.label5);
            this.groupBoxTests.Controls.Add(this.numericUpDownChannel2);
            this.groupBoxTests.Controls.Add(this.numericUpDownChannel);
            this.groupBoxTests.Location = new System.Drawing.Point(7, 94);
            this.groupBoxTests.Name = "groupBoxTests";
            this.groupBoxTests.Size = new System.Drawing.Size(774, 343);
            this.groupBoxTests.TabIndex = 10;
            this.groupBoxTests.TabStop = false;
            this.groupBoxTests.Text = "Tests";
            // 
            // buttonTestTriggerOutClockOut
            // 
            this.buttonTestTriggerOutClockOut.Location = new System.Drawing.Point(15, 249);
            this.buttonTestTriggerOutClockOut.Name = "buttonTestTriggerOutClockOut";
            this.buttonTestTriggerOutClockOut.Size = new System.Drawing.Size(186, 28);
            this.buttonTestTriggerOutClockOut.TabIndex = 0;
            this.buttonTestTriggerOutClockOut.Text = "Run TriggerOut-ClockOut Demo";
            this.buttonTestTriggerOutClockOut.UseVisualStyleBackColor = true;
            this.buttonTestTriggerOutClockOut.Click += new System.EventHandler(this.buttonTestTriggerOutClockOut_Click);
            // 
            // buttonTestFrequencyModulation
            // 
            this.buttonTestFrequencyModulation.Location = new System.Drawing.Point(15, 215);
            this.buttonTestFrequencyModulation.Name = "buttonTestFrequencyModulation";
            this.buttonTestFrequencyModulation.Size = new System.Drawing.Size(186, 28);
            this.buttonTestFrequencyModulation.TabIndex = 0;
            this.buttonTestFrequencyModulation.Text = "Run FrequencyModulation Demo";
            this.buttonTestFrequencyModulation.UseVisualStyleBackColor = true;
            this.buttonTestFrequencyModulation.Click += new System.EventHandler(this.buttonTestFrequencyModulation_Click);
            // 
            // buttonTestWaveformContinuous
            // 
            this.buttonTestWaveformContinuous.Location = new System.Drawing.Point(15, 181);
            this.buttonTestWaveformContinuous.Name = "buttonTestWaveformContinuous";
            this.buttonTestWaveformContinuous.Size = new System.Drawing.Size(186, 28);
            this.buttonTestWaveformContinuous.TabIndex = 0;
            this.buttonTestWaveformContinuous.Text = "Run WaveformContinuous Demo";
            this.buttonTestWaveformContinuous.UseVisualStyleBackColor = true;
            this.buttonTestWaveformContinuous.Click += new System.EventHandler(this.buttonTestWaveformContinuous_Click);
            // 
            // buttonTestAMmodulation
            // 
            this.buttonTestAMmodulation.Location = new System.Drawing.Point(15, 147);
            this.buttonTestAMmodulation.Name = "buttonTestAMmodulation";
            this.buttonTestAMmodulation.Size = new System.Drawing.Size(186, 28);
            this.buttonTestAMmodulation.TabIndex = 0;
            this.buttonTestAMmodulation.Text = "Run AMmodulation Demo";
            this.buttonTestAMmodulation.UseVisualStyleBackColor = true;
            this.buttonTestAMmodulation.Click += new System.EventHandler(this.buttonTestAMmodulation_Click);
            // 
            // buttonTestMultipleWaveforms
            // 
            this.buttonTestMultipleWaveforms.Location = new System.Drawing.Point(15, 113);
            this.buttonTestMultipleWaveforms.Name = "buttonTestMultipleWaveforms";
            this.buttonTestMultipleWaveforms.Size = new System.Drawing.Size(186, 28);
            this.buttonTestMultipleWaveforms.TabIndex = 0;
            this.buttonTestMultipleWaveforms.Text = "Run MultipleWaveforms Demo";
            this.buttonTestMultipleWaveforms.UseVisualStyleBackColor = true;
            this.buttonTestMultipleWaveforms.Click += new System.EventHandler(this.buttonTestMultipleWaveforms_Click);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(12, 48);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(55, 13);
            this.label6.TabIndex = 1;
            this.label6.Text = "Channel 2";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 22);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(46, 13);
            this.label5.TabIndex = 1;
            this.label5.Text = "Channel";
            // 
            // numericUpDownChannel2
            // 
            this.numericUpDownChannel2.Location = new System.Drawing.Point(73, 46);
            this.numericUpDownChannel2.Name = "numericUpDownChannel2";
            this.numericUpDownChannel2.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownChannel2.TabIndex = 3;
            this.numericUpDownChannel2.ValueChanged += new System.EventHandler(this.numericUpDownChannel_ValueChanged);
            // 
            // numericUpDownChannel
            // 
            this.numericUpDownChannel.Location = new System.Drawing.Point(73, 19);
            this.numericUpDownChannel.Name = "numericUpDownChannel";
            this.numericUpDownChannel.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownChannel.TabIndex = 3;
            this.numericUpDownChannel.ValueChanged += new System.EventHandler(this.numericUpDownChannel_ValueChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(792, 441);
            this.Controls.Add(this.groupBoxTests);
            this.Controls.Add(this.groupBox2);
            this.Name = "Form1";
            this.Text = "AOU Demo Launcher";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownSlot)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChassis)).EndInit();
            this.groupBoxTests.ResumeLayout(false);
            this.groupBoxTests.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChannel2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChannel)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button buttonTestWaveformTrigger;
        private System.Windows.Forms.TextBox textBoxOutput;
        private System.Windows.Forms.Button buttonContinue;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.Button buttonClose;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown numericUpDownSlot;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.NumericUpDown numericUpDownChassis;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox textBoxName;
        private System.Windows.Forms.GroupBox groupBoxTests;
        private System.Windows.Forms.Button buttonOpen;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown numericUpDownChannel;
        private System.Windows.Forms.Button buttonTestMultipleWaveforms;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.NumericUpDown numericUpDownChannel2;
        private System.Windows.Forms.Button buttonTestAMmodulation;
        private System.Windows.Forms.Button buttonTestWaveformContinuous;
        private System.Windows.Forms.Button buttonTestFrequencyModulation;
        private System.Windows.Forms.Button buttonTestTriggerOutClockOut;
    }
}

