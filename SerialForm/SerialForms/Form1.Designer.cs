namespace SerialForms
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.comboBoxSerial = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.textBoxLog = new System.Windows.Forms.TextBox();
            this.buttonPortStatus = new System.Windows.Forms.Button();
            this.labelStatus = new System.Windows.Forms.Label();
            this.buttonBrowser = new System.Windows.Forms.Button();
            this.SuspendLayout();
            //
            // comboBoxSerial
            //
            this.comboBoxSerial.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxSerial.FormattingEnabled = true;
            this.comboBoxSerial.Location = new System.Drawing.Point(59, 12);
            this.comboBoxSerial.Name = "comboBoxSerial";
            this.comboBoxSerial.Size = new System.Drawing.Size(121, 20);
            this.comboBoxSerial.TabIndex = 0;
            //
            // label1
            //
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 15);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 12);
            this.label1.TabIndex = 1;
            this.label1.Text = "串口：";
            //
            // textBoxLog
            //
            this.textBoxLog.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxLog.Location = new System.Drawing.Point(12, 61);
            this.textBoxLog.Multiline = true;
            this.textBoxLog.Name = "textBoxLog";
            this.textBoxLog.ReadOnly = true;
            this.textBoxLog.Size = new System.Drawing.Size(735, 447);
            this.textBoxLog.TabIndex = 2;
            //
            // buttonPortStatus
            //
            this.buttonPortStatus.Location = new System.Drawing.Point(186, 10);
            this.buttonPortStatus.Name = "buttonPortStatus";
            this.buttonPortStatus.Size = new System.Drawing.Size(75, 23);
            this.buttonPortStatus.TabIndex = 3;
            this.buttonPortStatus.Text = "查看状态";
            this.buttonPortStatus.UseVisualStyleBackColor = true;
            this.buttonPortStatus.Click += new System.EventHandler(this.buttonPortStatus_Click);
            //
            // labelStatus
            //
            this.labelStatus.AutoSize = true;
            this.labelStatus.Location = new System.Drawing.Point(267, 15);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(0, 12);
            this.labelStatus.TabIndex = 4;
            //
            // buttonBrowser
            //
            this.buttonBrowser.Location = new System.Drawing.Point(273, 10);
            this.buttonBrowser.Name = "buttonBrowser";
            this.buttonBrowser.Size = new System.Drawing.Size(88, 23);
            this.buttonBrowser.TabIndex = 5;
            this.buttonBrowser.Text = "启动浏览器";
            this.buttonBrowser.UseVisualStyleBackColor = true;
            this.buttonBrowser.Click += new System.EventHandler(this.buttonBrowser_Click);
            //
            // Form1
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(759, 520);
            this.Controls.Add(this.buttonBrowser);
            this.Controls.Add(this.labelStatus);
            this.Controls.Add(this.buttonPortStatus);
            this.Controls.Add(this.textBoxLog);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.comboBoxSerial);
            this.Name = "Form1";
            this.Text = "Form1";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox comboBoxSerial;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBoxLog;
        private System.Windows.Forms.Button buttonPortStatus;
        private System.Windows.Forms.Label labelStatus;
        private System.Windows.Forms.Button buttonBrowser;
    }
}

