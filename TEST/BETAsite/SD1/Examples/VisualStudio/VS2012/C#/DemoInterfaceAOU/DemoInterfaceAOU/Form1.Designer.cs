namespace AOU_Demo
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
            this.ButtonOpen = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.textBoxName = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.numericUpDownChassis = new System.Windows.Forms.NumericUpDown();
            this.numericUpDownSlot = new System.Windows.Forms.NumericUpDown();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.buttonClose = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.groupBoxChannel = new System.Windows.Forms.GroupBox();
            this.buttonResetPhase = new System.Windows.Forms.Button();
            this.checkBoxRstCh3 = new System.Windows.Forms.CheckBox();
            this.checkBoxRstCh1 = new System.Windows.Forms.CheckBox();
            this.checkBoxRstCh2 = new System.Windows.Forms.CheckBox();
            this.checkBoxRstCh0 = new System.Windows.Forms.CheckBox();
            this.buttonResetPhases = new System.Windows.Forms.Button();
            this.numericUpDownPhase = new System.Windows.Forms.NumericUpDown();
            this.numericUpDownOffset = new System.Windows.Forms.NumericUpDown();
            this.label14 = new System.Windows.Forms.Label();
            this.numericUpDownFrequency = new System.Windows.Forms.NumericUpDown();
            this.label9 = new System.Windows.Forms.Label();
            this.numericUpDownAmplitude = new System.Windows.Forms.NumericUpDown();
            this.label8 = new System.Windows.Forms.Label();
            this.comboBoxWaveShape = new System.Windows.Forms.ComboBox();
            this.label7 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.comboBoxChannel = new System.Windows.Forms.ComboBox();
            this.label5 = new System.Windows.Forms.Label();
            this.groupBoxAWG = new System.Windows.Forms.GroupBox();
            this.textBoxWFQueueList = new System.Windows.Forms.TextBox();
            this.textBoxWFModuleList = new System.Windows.Forms.TextBox();
            this.buttonStop = new System.Windows.Forms.Button();
            this.buttonPlay = new System.Windows.Forms.Button();
            this.buttonFlushQueue = new System.Windows.Forms.Button();
            this.buttonQueue = new System.Windows.Forms.Button();
            this.buttonFlushModule = new System.Windows.Forms.Button();
            this.buttonLoadInternal = new System.Windows.Forms.Button();
            this.buttonLoadWaveform = new System.Windows.Forms.Button();
            this.buttonBrowse = new System.Windows.Forms.Button();
            this.textBoxFileName = new System.Windows.Forms.TextBox();
            this.numericUpDownPrescaler = new System.Windows.Forms.NumericUpDown();
            this.label11 = new System.Windows.Forms.Label();
            this.numericUpDownWFnumber = new System.Windows.Forms.NumericUpDown();
            this.numericUpDownCycles = new System.Windows.Forms.NumericUpDown();
            this.labelWaveformsInModule = new System.Windows.Forms.Label();
            this.labelWaveformsInQueue = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.groupBoxModulation = new System.Windows.Forms.GroupBox();
            this.comboBoxModulation = new System.Windows.Forms.ComboBox();
            this.label12 = new System.Windows.Forms.Label();
            this.numericUpDownDevGain = new System.Windows.Forms.NumericUpDown();
            this.labelDevGain = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChassis)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownSlot)).BeginInit();
            this.groupBoxChannel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPhase)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownOffset)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownFrequency)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownAmplitude)).BeginInit();
            this.groupBoxAWG.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPrescaler)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownWFnumber)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownCycles)).BeginInit();
            this.groupBoxModulation.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownDevGain)).BeginInit();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // ButtonOpen
            // 
            this.ButtonOpen.Location = new System.Drawing.Point(28, 43);
            this.ButtonOpen.Name = "ButtonOpen";
            this.ButtonOpen.Size = new System.Drawing.Size(77, 24);
            this.ButtonOpen.TabIndex = 0;
            this.ButtonOpen.Text = "Open";
            this.ButtonOpen.UseVisualStyleBackColor = true;
            this.ButtonOpen.Click += new System.EventHandler(this.buttonOpen_Click);
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
            // textBoxName
            // 
            this.textBoxName.Location = new System.Drawing.Point(56, 19);
            this.textBoxName.Name = "textBoxName";
            this.textBoxName.Size = new System.Drawing.Size(167, 20);
            this.textBoxName.TabIndex = 2;
            this.textBoxName.Text = "SD-PXE-AOU-H0002";
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
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(353, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(25, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "Slot";
            // 
            // numericUpDownChassis
            // 
            this.numericUpDownChassis.Location = new System.Drawing.Point(288, 20);
            this.numericUpDownChassis.Name = "numericUpDownChassis";
            this.numericUpDownChassis.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownChassis.TabIndex = 3;
            // 
            // numericUpDownSlot
            // 
            this.numericUpDownSlot.Location = new System.Drawing.Point(384, 20);
            this.numericUpDownSlot.Name = "numericUpDownSlot";
            this.numericUpDownSlot.Size = new System.Drawing.Size(51, 20);
            this.numericUpDownSlot.TabIndex = 3;
            this.numericUpDownSlot.Value = new decimal(new int[] {
            2,
            0,
            0,
            0});
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
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(219, 49);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(37, 13);
            this.label4.TabIndex = 1;
            this.label4.Text = "Status";
            // 
            // groupBoxChannel
            // 
            this.groupBoxChannel.Controls.Add(this.buttonResetPhase);
            this.groupBoxChannel.Controls.Add(this.checkBoxRstCh3);
            this.groupBoxChannel.Controls.Add(this.checkBoxRstCh1);
            this.groupBoxChannel.Controls.Add(this.checkBoxRstCh2);
            this.groupBoxChannel.Controls.Add(this.checkBoxRstCh0);
            this.groupBoxChannel.Controls.Add(this.buttonResetPhases);
            this.groupBoxChannel.Controls.Add(this.numericUpDownPhase);
            this.groupBoxChannel.Controls.Add(this.numericUpDownOffset);
            this.groupBoxChannel.Controls.Add(this.label14);
            this.groupBoxChannel.Controls.Add(this.numericUpDownFrequency);
            this.groupBoxChannel.Controls.Add(this.label9);
            this.groupBoxChannel.Controls.Add(this.numericUpDownAmplitude);
            this.groupBoxChannel.Controls.Add(this.label8);
            this.groupBoxChannel.Controls.Add(this.comboBoxWaveShape);
            this.groupBoxChannel.Controls.Add(this.label7);
            this.groupBoxChannel.Controls.Add(this.label6);
            this.groupBoxChannel.Controls.Add(this.comboBoxChannel);
            this.groupBoxChannel.Controls.Add(this.label5);
            this.groupBoxChannel.Location = new System.Drawing.Point(12, 95);
            this.groupBoxChannel.Name = "groupBoxChannel";
            this.groupBoxChannel.Size = new System.Drawing.Size(445, 142);
            this.groupBoxChannel.TabIndex = 5;
            this.groupBoxChannel.TabStop = false;
            this.groupBoxChannel.Text = "Channel Control";
            // 
            // buttonResetPhase
            // 
            this.buttonResetPhase.Location = new System.Drawing.Point(111, 22);
            this.buttonResetPhase.Name = "buttonResetPhase";
            this.buttonResetPhase.Size = new System.Drawing.Size(109, 21);
            this.buttonResetPhase.TabIndex = 6;
            this.buttonResetPhase.Text = "Reset Acc. Phase";
            this.buttonResetPhase.UseVisualStyleBackColor = true;
            this.buttonResetPhase.Click += new System.EventHandler(this.buttonResetPhase_Click);
            // 
            // checkBoxRstCh3
            // 
            this.checkBoxRstCh3.AutoSize = true;
            this.checkBoxRstCh3.Location = new System.Drawing.Point(384, 48);
            this.checkBoxRstCh3.Name = "checkBoxRstCh3";
            this.checkBoxRstCh3.Size = new System.Drawing.Size(45, 17);
            this.checkBoxRstCh3.TabIndex = 5;
            this.checkBoxRstCh3.Text = "Ch3";
            this.checkBoxRstCh3.UseVisualStyleBackColor = true;
            // 
            // checkBoxRstCh1
            // 
            this.checkBoxRstCh1.AutoSize = true;
            this.checkBoxRstCh1.Location = new System.Drawing.Point(384, 25);
            this.checkBoxRstCh1.Name = "checkBoxRstCh1";
            this.checkBoxRstCh1.Size = new System.Drawing.Size(45, 17);
            this.checkBoxRstCh1.TabIndex = 5;
            this.checkBoxRstCh1.Text = "Ch1";
            this.checkBoxRstCh1.UseVisualStyleBackColor = true;
            // 
            // checkBoxRstCh2
            // 
            this.checkBoxRstCh2.AutoSize = true;
            this.checkBoxRstCh2.Location = new System.Drawing.Point(333, 48);
            this.checkBoxRstCh2.Name = "checkBoxRstCh2";
            this.checkBoxRstCh2.Size = new System.Drawing.Size(45, 17);
            this.checkBoxRstCh2.TabIndex = 5;
            this.checkBoxRstCh2.Text = "Ch2";
            this.checkBoxRstCh2.UseVisualStyleBackColor = true;
            // 
            // checkBoxRstCh0
            // 
            this.checkBoxRstCh0.AutoSize = true;
            this.checkBoxRstCh0.Location = new System.Drawing.Point(333, 25);
            this.checkBoxRstCh0.Name = "checkBoxRstCh0";
            this.checkBoxRstCh0.Size = new System.Drawing.Size(45, 17);
            this.checkBoxRstCh0.TabIndex = 5;
            this.checkBoxRstCh0.Text = "Ch0";
            this.checkBoxRstCh0.UseVisualStyleBackColor = true;
            // 
            // buttonResetPhases
            // 
            this.buttonResetPhases.Location = new System.Drawing.Point(246, 19);
            this.buttonResetPhases.Name = "buttonResetPhases";
            this.buttonResetPhases.Size = new System.Drawing.Size(80, 51);
            this.buttonResetPhases.TabIndex = 4;
            this.buttonResetPhases.Text = "Reset Accumulated Phases";
            this.buttonResetPhases.UseVisualStyleBackColor = true;
            this.buttonResetPhases.Click += new System.EventHandler(this.buttonResetPhases_Click);
            // 
            // numericUpDownPhase
            // 
            this.numericUpDownPhase.DecimalPlaces = 3;
            this.numericUpDownPhase.Increment = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.numericUpDownPhase.Location = new System.Drawing.Point(288, 108);
            this.numericUpDownPhase.Maximum = new decimal(new int[] {
            360,
            0,
            0,
            0});
            this.numericUpDownPhase.Minimum = new decimal(new int[] {
            360,
            0,
            0,
            -2147483648});
            this.numericUpDownPhase.Name = "numericUpDownPhase";
            this.numericUpDownPhase.Size = new System.Drawing.Size(120, 20);
            this.numericUpDownPhase.TabIndex = 3;
            this.numericUpDownPhase.ValueChanged += new System.EventHandler(this.numericUpDownPhase_ValueChanged);
            // 
            // numericUpDownOffset
            // 
            this.numericUpDownOffset.DecimalPlaces = 3;
            this.numericUpDownOffset.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.numericUpDownOffset.Location = new System.Drawing.Point(288, 82);
            this.numericUpDownOffset.Maximum = new decimal(new int[] {
            15,
            0,
            0,
            65536});
            this.numericUpDownOffset.Minimum = new decimal(new int[] {
            15,
            0,
            0,
            -2147418112});
            this.numericUpDownOffset.Name = "numericUpDownOffset";
            this.numericUpDownOffset.Size = new System.Drawing.Size(120, 20);
            this.numericUpDownOffset.TabIndex = 3;
            this.numericUpDownOffset.ValueChanged += new System.EventHandler(this.numericUpDownOffset_ValueChanged);
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(243, 110);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(37, 13);
            this.label14.TabIndex = 1;
            this.label14.Text = "Phase";
            // 
            // numericUpDownFrequency
            // 
            this.numericUpDownFrequency.DecimalPlaces = 3;
            this.numericUpDownFrequency.Increment = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.numericUpDownFrequency.Location = new System.Drawing.Point(100, 108);
            this.numericUpDownFrequency.Maximum = new decimal(new int[] {
            200,
            0,
            0,
            0});
            this.numericUpDownFrequency.Name = "numericUpDownFrequency";
            this.numericUpDownFrequency.Size = new System.Drawing.Size(120, 20);
            this.numericUpDownFrequency.TabIndex = 3;
            this.numericUpDownFrequency.ValueChanged += new System.EventHandler(this.numericUpDownFrequency_ValueChanged);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(243, 84);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(35, 13);
            this.label9.TabIndex = 1;
            this.label9.Text = "Offset";
            // 
            // numericUpDownAmplitude
            // 
            this.numericUpDownAmplitude.DecimalPlaces = 3;
            this.numericUpDownAmplitude.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.numericUpDownAmplitude.Location = new System.Drawing.Point(100, 82);
            this.numericUpDownAmplitude.Maximum = new decimal(new int[] {
            15,
            0,
            0,
            65536});
            this.numericUpDownAmplitude.Minimum = new decimal(new int[] {
            15,
            0,
            0,
            -2147418112});
            this.numericUpDownAmplitude.Name = "numericUpDownAmplitude";
            this.numericUpDownAmplitude.Size = new System.Drawing.Size(120, 20);
            this.numericUpDownAmplitude.TabIndex = 3;
            this.numericUpDownAmplitude.ValueChanged += new System.EventHandler(this.numericUpDownAmplitude_ValueChanged);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(6, 110);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(88, 13);
            this.label8.TabIndex = 1;
            this.label8.Text = "Frequency (MHz)";
            // 
            // comboBoxWaveShape
            // 
            this.comboBoxWaveShape.FormattingEnabled = true;
            this.comboBoxWaveShape.Items.AddRange(new object[] {
            "Off",
            "Sinusoidal",
            "Triangular",
            "Square",
            "DC",
            "AWG"});
            this.comboBoxWaveShape.Location = new System.Drawing.Point(100, 54);
            this.comboBoxWaveShape.Name = "comboBoxWaveShape";
            this.comboBoxWaveShape.Size = new System.Drawing.Size(121, 21);
            this.comboBoxWaveShape.TabIndex = 2;
            this.comboBoxWaveShape.Text = "Off";
            this.comboBoxWaveShape.SelectedIndexChanged += new System.EventHandler(this.comboBoxWaveShape_SelectedIndexChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(6, 84);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(53, 13);
            this.label7.TabIndex = 1;
            this.label7.Text = "Amplitude";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(6, 57);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(67, 13);
            this.label6.TabIndex = 1;
            this.label6.Text = "WaveShape";
            // 
            // comboBoxChannel
            // 
            this.comboBoxChannel.FormattingEnabled = true;
            this.comboBoxChannel.Items.AddRange(new object[] {
            "0",
            "1",
            "2",
            "3"});
            this.comboBoxChannel.Location = new System.Drawing.Point(58, 22);
            this.comboBoxChannel.Name = "comboBoxChannel";
            this.comboBoxChannel.Size = new System.Drawing.Size(37, 21);
            this.comboBoxChannel.TabIndex = 2;
            this.comboBoxChannel.Text = "0";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(6, 25);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(46, 13);
            this.label5.TabIndex = 1;
            this.label5.Text = "Channel";
            // 
            // groupBoxAWG
            // 
            this.groupBoxAWG.Controls.Add(this.textBoxWFQueueList);
            this.groupBoxAWG.Controls.Add(this.textBoxWFModuleList);
            this.groupBoxAWG.Controls.Add(this.buttonStop);
            this.groupBoxAWG.Controls.Add(this.buttonPlay);
            this.groupBoxAWG.Controls.Add(this.buttonFlushQueue);
            this.groupBoxAWG.Controls.Add(this.buttonQueue);
            this.groupBoxAWG.Controls.Add(this.buttonFlushModule);
            this.groupBoxAWG.Controls.Add(this.buttonLoadInternal);
            this.groupBoxAWG.Controls.Add(this.buttonLoadWaveform);
            this.groupBoxAWG.Controls.Add(this.buttonBrowse);
            this.groupBoxAWG.Controls.Add(this.textBoxFileName);
            this.groupBoxAWG.Controls.Add(this.numericUpDownPrescaler);
            this.groupBoxAWG.Controls.Add(this.label11);
            this.groupBoxAWG.Controls.Add(this.numericUpDownWFnumber);
            this.groupBoxAWG.Controls.Add(this.numericUpDownCycles);
            this.groupBoxAWG.Controls.Add(this.labelWaveformsInModule);
            this.groupBoxAWG.Controls.Add(this.labelWaveformsInQueue);
            this.groupBoxAWG.Controls.Add(this.label13);
            this.groupBoxAWG.Controls.Add(this.label10);
            this.groupBoxAWG.Location = new System.Drawing.Point(12, 308);
            this.groupBoxAWG.Name = "groupBoxAWG";
            this.groupBoxAWG.Size = new System.Drawing.Size(445, 457);
            this.groupBoxAWG.TabIndex = 6;
            this.groupBoxAWG.TabStop = false;
            this.groupBoxAWG.Text = "AWG Control";
            // 
            // textBoxWFQueueList
            // 
            this.textBoxWFQueueList.Location = new System.Drawing.Point(7, 276);
            this.textBoxWFQueueList.Multiline = true;
            this.textBoxWFQueueList.Name = "textBoxWFQueueList";
            this.textBoxWFQueueList.Size = new System.Drawing.Size(420, 138);
            this.textBoxWFQueueList.TabIndex = 6;
            // 
            // textBoxWFModuleList
            // 
            this.textBoxWFModuleList.Location = new System.Drawing.Point(7, 77);
            this.textBoxWFModuleList.Multiline = true;
            this.textBoxWFModuleList.Name = "textBoxWFModuleList";
            this.textBoxWFModuleList.Size = new System.Drawing.Size(420, 138);
            this.textBoxWFModuleList.TabIndex = 6;
            // 
            // buttonStop
            // 
            this.buttonStop.Location = new System.Drawing.Point(88, 427);
            this.buttonStop.Name = "buttonStop";
            this.buttonStop.Size = new System.Drawing.Size(75, 23);
            this.buttonStop.TabIndex = 5;
            this.buttonStop.Text = "Stop";
            this.buttonStop.UseVisualStyleBackColor = true;
            this.buttonStop.Click += new System.EventHandler(this.buttonStop_Click);
            // 
            // buttonPlay
            // 
            this.buttonPlay.Location = new System.Drawing.Point(7, 428);
            this.buttonPlay.Name = "buttonPlay";
            this.buttonPlay.Size = new System.Drawing.Size(75, 23);
            this.buttonPlay.TabIndex = 5;
            this.buttonPlay.Text = "Play";
            this.buttonPlay.UseVisualStyleBackColor = true;
            this.buttonPlay.Click += new System.EventHandler(this.buttonPlay_Click);
            // 
            // buttonFlushQueue
            // 
            this.buttonFlushQueue.Location = new System.Drawing.Point(65, 247);
            this.buttonFlushQueue.Name = "buttonFlushQueue";
            this.buttonFlushQueue.Size = new System.Drawing.Size(58, 23);
            this.buttonFlushQueue.TabIndex = 4;
            this.buttonFlushQueue.Text = "Flush";
            this.buttonFlushQueue.UseVisualStyleBackColor = true;
            this.buttonFlushQueue.Click += new System.EventHandler(this.buttonFlushQueue_Click);
            // 
            // buttonQueue
            // 
            this.buttonQueue.Location = new System.Drawing.Point(10, 247);
            this.buttonQueue.Name = "buttonQueue";
            this.buttonQueue.Size = new System.Drawing.Size(49, 23);
            this.buttonQueue.TabIndex = 4;
            this.buttonQueue.Text = "Queue";
            this.buttonQueue.UseVisualStyleBackColor = true;
            this.buttonQueue.Click += new System.EventHandler(this.buttonQueue_Click);
            // 
            // buttonFlushModule
            // 
            this.buttonFlushModule.Location = new System.Drawing.Point(111, 47);
            this.buttonFlushModule.Name = "buttonFlushModule";
            this.buttonFlushModule.Size = new System.Drawing.Size(85, 23);
            this.buttonFlushModule.TabIndex = 2;
            this.buttonFlushModule.Text = "Flush Module";
            this.buttonFlushModule.UseVisualStyleBackColor = true;
            this.buttonFlushModule.Click += new System.EventHandler(this.buttonFlushModule_Click);
            // 
            // buttonLoadInternal
            // 
            this.buttonLoadInternal.Location = new System.Drawing.Point(334, 47);
            this.buttonLoadInternal.Name = "buttonLoadInternal";
            this.buttonLoadInternal.Size = new System.Drawing.Size(93, 23);
            this.buttonLoadInternal.TabIndex = 2;
            this.buttonLoadInternal.Text = "Load Internal";
            this.buttonLoadInternal.UseVisualStyleBackColor = true;
            this.buttonLoadInternal.Click += new System.EventHandler(this.buttonLoadInternal_Click);
            // 
            // buttonLoadWaveform
            // 
            this.buttonLoadWaveform.Location = new System.Drawing.Point(7, 47);
            this.buttonLoadWaveform.Name = "buttonLoadWaveform";
            this.buttonLoadWaveform.Size = new System.Drawing.Size(98, 23);
            this.buttonLoadWaveform.TabIndex = 2;
            this.buttonLoadWaveform.Text = "Load to Module";
            this.buttonLoadWaveform.UseVisualStyleBackColor = true;
            this.buttonLoadWaveform.Click += new System.EventHandler(this.buttonLoadWaveform_Click);
            // 
            // buttonBrowse
            // 
            this.buttonBrowse.Location = new System.Drawing.Point(400, 16);
            this.buttonBrowse.Name = "buttonBrowse";
            this.buttonBrowse.Size = new System.Drawing.Size(27, 20);
            this.buttonBrowse.TabIndex = 1;
            this.buttonBrowse.Text = "...";
            this.buttonBrowse.UseVisualStyleBackColor = true;
            this.buttonBrowse.Click += new System.EventHandler(this.buttonBrowse_Click);
            // 
            // textBoxFileName
            // 
            this.textBoxFileName.Location = new System.Drawing.Point(7, 17);
            this.textBoxFileName.Name = "textBoxFileName";
            this.textBoxFileName.Size = new System.Drawing.Size(387, 20);
            this.textBoxFileName.TabIndex = 0;
            // 
            // numericUpDownPrescaler
            // 
            this.numericUpDownPrescaler.Location = new System.Drawing.Point(278, 221);
            this.numericUpDownPrescaler.Maximum = new decimal(new int[] {
            4095,
            0,
            0,
            0});
            this.numericUpDownPrescaler.Name = "numericUpDownPrescaler";
            this.numericUpDownPrescaler.Size = new System.Drawing.Size(61, 20);
            this.numericUpDownPrescaler.TabIndex = 3;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(221, 223);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(51, 13);
            this.label11.TabIndex = 1;
            this.label11.Text = "Prescaler";
            // 
            // numericUpDownWFnumber
            // 
            this.numericUpDownWFnumber.Location = new System.Drawing.Point(49, 221);
            this.numericUpDownWFnumber.Maximum = new decimal(new int[] {
            4095,
            0,
            0,
            0});
            this.numericUpDownWFnumber.Name = "numericUpDownWFnumber";
            this.numericUpDownWFnumber.Size = new System.Drawing.Size(45, 20);
            this.numericUpDownWFnumber.TabIndex = 3;
            // 
            // numericUpDownCycles
            // 
            this.numericUpDownCycles.Location = new System.Drawing.Point(152, 221);
            this.numericUpDownCycles.Maximum = new decimal(new int[] {
            4095,
            0,
            0,
            0});
            this.numericUpDownCycles.Name = "numericUpDownCycles";
            this.numericUpDownCycles.Size = new System.Drawing.Size(58, 20);
            this.numericUpDownCycles.TabIndex = 3;
            // 
            // labelWaveformsInModule
            // 
            this.labelWaveformsInModule.AutoSize = true;
            this.labelWaveformsInModule.Location = new System.Drawing.Point(202, 52);
            this.labelWaveformsInModule.Name = "labelWaveformsInModule";
            this.labelWaveformsInModule.Size = new System.Drawing.Size(122, 13);
            this.labelWaveformsInModule.TabIndex = 1;
            this.labelWaveformsInModule.Text = "Waveforms in Module: 0";
            // 
            // labelWaveformsInQueue
            // 
            this.labelWaveformsInQueue.AutoSize = true;
            this.labelWaveformsInQueue.Location = new System.Drawing.Point(129, 252);
            this.labelWaveformsInQueue.Name = "labelWaveformsInQueue";
            this.labelWaveformsInQueue.Size = new System.Drawing.Size(119, 13);
            this.labelWaveformsInQueue.TabIndex = 1;
            this.labelWaveformsInQueue.Text = "Waveforms in Queue: 0";
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(12, 223);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(31, 13);
            this.label13.TabIndex = 1;
            this.label13.Text = "WF#";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(108, 223);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(38, 13);
            this.label10.TabIndex = 1;
            this.label10.Text = "Cycles";
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.Filter = "Waveform File | *.csv";
            // 
            // groupBoxModulation
            // 
            this.groupBoxModulation.Controls.Add(this.comboBoxModulation);
            this.groupBoxModulation.Controls.Add(this.label12);
            this.groupBoxModulation.Controls.Add(this.numericUpDownDevGain);
            this.groupBoxModulation.Controls.Add(this.labelDevGain);
            this.groupBoxModulation.Location = new System.Drawing.Point(12, 243);
            this.groupBoxModulation.Name = "groupBoxModulation";
            this.groupBoxModulation.Size = new System.Drawing.Size(445, 59);
            this.groupBoxModulation.TabIndex = 7;
            this.groupBoxModulation.TabStop = false;
            this.groupBoxModulation.Text = "Modulation Control";
            // 
            // comboBoxModulation
            // 
            this.comboBoxModulation.FormattingEnabled = true;
            this.comboBoxModulation.Items.AddRange(new object[] {
            "Off",
            "Amplitude",
            "Frequency",
            "Phase",
            "IQ"});
            this.comboBoxModulation.Location = new System.Drawing.Point(101, 25);
            this.comboBoxModulation.Name = "comboBoxModulation";
            this.comboBoxModulation.Size = new System.Drawing.Size(111, 21);
            this.comboBoxModulation.TabIndex = 2;
            this.comboBoxModulation.Text = "Off";
            this.comboBoxModulation.SelectedIndexChanged += new System.EventHandler(this.comboBoxModulation_SelectedIndexChanged);
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(9, 28);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(86, 13);
            this.label12.TabIndex = 1;
            this.label12.Text = "Modulation Type";
            // 
            // numericUpDownDevGain
            // 
            this.numericUpDownDevGain.DecimalPlaces = 3;
            this.numericUpDownDevGain.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.numericUpDownDevGain.Location = new System.Drawing.Point(310, 26);
            this.numericUpDownDevGain.Maximum = new decimal(new int[] {
            15,
            0,
            0,
            65536});
            this.numericUpDownDevGain.Minimum = new decimal(new int[] {
            15,
            0,
            0,
            -2147418112});
            this.numericUpDownDevGain.Name = "numericUpDownDevGain";
            this.numericUpDownDevGain.Size = new System.Drawing.Size(111, 20);
            this.numericUpDownDevGain.TabIndex = 3;
            this.numericUpDownDevGain.ValueChanged += new System.EventHandler(this.numericUpDownDevGain_ValueChanged);
            // 
            // labelDevGain
            // 
            this.labelDevGain.AutoSize = true;
            this.labelDevGain.Location = new System.Drawing.Point(227, 28);
            this.labelDevGain.Name = "labelDevGain";
            this.labelDevGain.Size = new System.Drawing.Size(77, 13);
            this.labelDevGain.TabIndex = 1;
            this.labelDevGain.Text = "Deviation Gain";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.textBoxStatus);
            this.groupBox2.Controls.Add(this.ButtonOpen);
            this.groupBox2.Controls.Add(this.buttonClose);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.numericUpDownSlot);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.numericUpDownChassis);
            this.groupBox2.Controls.Add(this.label4);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.textBoxName);
            this.groupBox2.Location = new System.Drawing.Point(12, 10);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(445, 79);
            this.groupBox2.TabIndex = 8;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Module Control";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(471, 775);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBoxModulation);
            this.Controls.Add(this.groupBoxAWG);
            this.Controls.Add(this.groupBoxChannel);
            this.Name = "Form1";
            this.Text = "Demo AOU";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownChassis)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownSlot)).EndInit();
            this.groupBoxChannel.ResumeLayout(false);
            this.groupBoxChannel.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPhase)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownOffset)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownFrequency)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownAmplitude)).EndInit();
            this.groupBoxAWG.ResumeLayout(false);
            this.groupBoxAWG.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPrescaler)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownWFnumber)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownCycles)).EndInit();
            this.groupBoxModulation.ResumeLayout(false);
            this.groupBoxModulation.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownDevGain)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button ButtonOpen;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBoxName;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown numericUpDownChassis;
        private System.Windows.Forms.NumericUpDown numericUpDownSlot;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.Button buttonClose;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.GroupBox groupBoxChannel;
        private System.Windows.Forms.NumericUpDown numericUpDownFrequency;
        private System.Windows.Forms.NumericUpDown numericUpDownAmplitude;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ComboBox comboBoxWaveShape;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ComboBox comboBoxChannel;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown numericUpDownOffset;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.GroupBox groupBoxAWG;
        private System.Windows.Forms.Button buttonPlay;
        private System.Windows.Forms.Button buttonFlushQueue;
        private System.Windows.Forms.Button buttonQueue;
        private System.Windows.Forms.Button buttonLoadWaveform;
        private System.Windows.Forms.Button buttonBrowse;
        private System.Windows.Forms.TextBox textBoxFileName;
        private System.Windows.Forms.NumericUpDown numericUpDownPrescaler;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.NumericUpDown numericUpDownCycles;
        private System.Windows.Forms.Label labelWaveformsInModule;
        private System.Windows.Forms.Label labelWaveformsInQueue;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Button buttonFlushModule;
        private System.Windows.Forms.NumericUpDown numericUpDownWFnumber;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Button buttonStop;
        private System.Windows.Forms.TextBox textBoxWFQueueList;
        private System.Windows.Forms.TextBox textBoxWFModuleList;
        private System.Windows.Forms.Button buttonLoadInternal;
        private System.Windows.Forms.GroupBox groupBoxModulation;
        private System.Windows.Forms.ComboBox comboBoxModulation;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.NumericUpDown numericUpDownDevGain;
        private System.Windows.Forms.Label labelDevGain;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.CheckBox checkBoxRstCh3;
        private System.Windows.Forms.CheckBox checkBoxRstCh1;
        private System.Windows.Forms.CheckBox checkBoxRstCh2;
        private System.Windows.Forms.CheckBox checkBoxRstCh0;
        private System.Windows.Forms.Button buttonResetPhases;
        private System.Windows.Forms.NumericUpDown numericUpDownPhase;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Button buttonResetPhase;
    }
}

