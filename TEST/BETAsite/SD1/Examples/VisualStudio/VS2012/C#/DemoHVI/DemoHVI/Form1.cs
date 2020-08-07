using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using KeysightSD1;

namespace DemoHVI
{
    public partial class Form1 : Form
    {
        private SD_HVI HVI;
        private SD_Module module;

        public Form1()
        {
            InitializeComponent();
            this.HVI = new SD_HVI();
            this.module = null;
        }

        private void HVIbutton_Click(object sender, EventArgs e)
        {
            OpenFileDialog dialog = new OpenFileDialog();
            dialog.Filter = "HVI Compiler Files (.HVI)|*.HVI";

            if (dialog.ShowDialog() == DialogResult.OK)
                this.HVIpath.Text = dialog.FileName;
        }

        private void openButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.open(this.HVIpath.Text)) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                this.openButton.Enabled = false;
                this.closeButton.Enabled = true;
                this.moduleButton.Enabled = true;
                this.startButton.Enabled = true;
                this.stopButton.Enabled = true;
                this.pauseButton.Enabled = true;
                this.resumeButton.Enabled = true;
            }
        }

        private void closeButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.close()) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                this.openButton.Enabled = true;
                this.closeButton.Enabled = false;
                this.startButton.Enabled = false;
                this.stopButton.Enabled = false;
                this.pauseButton.Enabled = false;
                this.resumeButton.Enabled = false;
                this.moduleButton.Enabled = false;
                this.module = null;
                this.readButton.Enabled = false;
                this.writeButton.Enabled = false;
                this.triggerRead.Enabled = false;
                this.triggerWrite.Enabled = false;
            }
        }

        private void startButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.start()) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void stopButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.stop()) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void pauseButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.pause()) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void resumeButton_Click(object sender, EventArgs e)
        {
            int error;

            if ((error = this.HVI.resume()) < 0)
                MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void moduleButton_Click(object sender, EventArgs e)
        {
            this.module = this.HVI.getModule(this.moduleName.Text);
            if (this.module != null)
            {
                this.readButton.Enabled = true;
                this.writeButton.Enabled = true;
                this.triggerRead.Enabled = true;
                this.triggerWrite.Enabled = true;
                this.moduleButton.Enabled = false;
            }
            else
                MessageBox.Show("Error", "Module \"" + this.moduleName.Text + "\" not found in HVI.", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void moduleName_TextChanged(object sender, EventArgs e)
        {
            this.module = null;
            this.moduleButton.Enabled = true;
            this.readButton.Enabled = false;
            this.writeButton.Enabled = false;
            this.triggerRead.Enabled = false;
            this.triggerWrite.Enabled = false;
        }

        private void writeButton_Click(object sender, EventArgs e)
        {
            int error;

            if(this.module == null)
                MessageBox.Show("Error", "No module owned.", MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                if ((error = this.module.writeRegister((int)(this.registerNumber.Value), (int)(this.value2write.Value))) < 0)
                    MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void readButton_Click(object sender, EventArgs e)
        {
            int error, value;

            if (this.module == null)
                MessageBox.Show("Error", "No module owned.", MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                value = this.module.readRegister((int)(this.registerNumber.Value), out error);
                if (error < 0)
                    MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
                else
                    this.readValue.Text = value.ToString();
            }
        }

        private void triggerWrite_Click(object sender, EventArgs e)
        {
            int error;

            if (this.module == null)
                MessageBox.Show("Error", "No module owned.", MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                if ((error = this.module.PXItriggerWrite((int)(this.registerNumber.Value), (int)(this.value2write.Value))) < 0)
                    MessageBox.Show("Error", SD_Error.getErrorMessage(error), MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void triggerRead_Click(object sender, EventArgs e)
        {
            int value;

            if (this.module == null)
                MessageBox.Show("Error", "No module owned.", MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                value = this.module.PXItriggerRead((int)(this.registerNumber.Value));
                if (value < 0)
                    MessageBox.Show("Error", SD_Error.getErrorMessage(value), MessageBoxButtons.OK, MessageBoxIcon.Error);
                else
                    this.readTrigger.Text = value.ToString();
            }
        }
    }
}
