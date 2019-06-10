using System;
using System.Diagnostics;
using System.IO.Ports;
using System.Windows.Forms;

namespace SerialForms
{
    public partial class Form1 : Form
    {
        ClassSerial classSerial;
        ClassWeb classWeb;
        public Form1()
        {
            classWeb = new ClassWeb(new ClassWeb.OnGetPost(onGetPost));
            classSerial = new ClassSerial();
            InitializeComponent();
            string[] ports = SerialPort.GetPortNames();
            foreach (string name in ports)
                comboBoxSerial.Items.Add(name);
            if (comboBoxSerial.Items.Count > 0)
                comboBoxSerial.SelectedIndex = 0;
        }

        private void buttonPortStatus_Click(object sender, EventArgs e)
        {
            string result = comboBoxSerial.Text;
            labelStatus.Text = result;
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            classWeb.close();
            classSerial.closeAllPort();
        }

        string onGetPost(string post)
        {
            if (post.StartsWith("get:"))
            {
                string[] list = post.Split(':');
                string getName = list[1];
                if (getName == "list")
                    return classSerial.portNameList;
                else if (getName == "port")
                    return classSerial.getPortStatus(list[2]);
                else if (getName == "openList")
                    return classSerial.getOpenList();
                else if (getName == "open")
                {
                    string result = classSerial.openPort(list[2], list[3]);
                    this.BeginInvoke(new ClassWeb.OnGetPost(updateLogText), new object[] { result });
                    return result;
                }
                else if (getName == "close")
                {
                    string result = classSerial.closePort(list[2]);
                    this.BeginInvoke(new ClassWeb.OnGetPost(updateLogText), new object[] { result });
                    return result;
                }
                else if (getName == "data")
                {
                    bool hasRemain = true;
                    string data = "";
                    while (hasRemain)
                    {
                        string result = ClassSerial.receiveData(out hasRemain);
                        if (result != null && result.Length > 0)
                            data += result + "\r\n";
                    }
                    if (data.Length > 0)
                        this.BeginInvoke(new ClassWeb.OnGetPost(updateLogText), new object[] { data });
                    return "{\"data\": \"" + data + "\"}";
                }
            }
            return "";
        }

        private void buttonBrowser_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("explorer.exe", "http://127.0.0.1:8000");
        }

        string updateLogText(string log)
        {
            textBoxLog.Text = log + "\r\n" + textBoxLog.Text;
            return "";
        }

        private void Form1_Shown(object sender, EventArgs e)
        {
            startWebServer();
        }

        void startWebServer()
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = Environment.CurrentDirectory + "\\startup.bat";
            Process myPro = new Process();
            myPro.StartInfo = start;
            myPro.Start();
        }

        private void buttonWebServerStart_Click(object sender, EventArgs e)
        {
            startWebServer();
        }
    }
}
