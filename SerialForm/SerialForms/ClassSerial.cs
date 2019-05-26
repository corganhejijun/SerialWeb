using System.Collections;
using System.IO.Ports;

namespace SerialForms
{
    class ClassSerial
    {
        SerialPort[] portList;
        ArrayList openedList;
        public ClassSerial()
        {
            string[] portNames = SerialPort.GetPortNames();
            portList = new SerialPort[portNames.Length];
            for (int i = 0; i < portList.Length; i++)
            {
                SerialPort port = new SerialPort(portNames[i]);
                portList[i] = port;
            }
            openedList = new ArrayList();
        }

        public string portNameList
        {
            get
            {
                string nameList = "[";
                for (int i = 0; i < portList.Length; i++)
                    nameList += "[\"" + portList[i].PortName + "\"],";
                nameList = nameList.Substring(0, nameList.Length - 1);  // delete the last ,
                nameList = "{\"port\":" + nameList + "]}";
                return nameList;
            }
        }

        public string getPortStatus(string name)
        {
            string result = "{";
            string opened = "\"opened\":false";
            foreach (SerialPort port in openedList)
            {
                if (port.PortName == "name")
                {
                    opened = "\"opened\":true";
                }
            }
            string occupy = "\"occupy\":false";
            foreach (SerialPort port in portList)
            {
                if (openedList.Contains(port))
                    continue;
                if (port.IsOpen)
                    occupy = "\"occupy\":true";
            }
            result += opened + ',' + occupy;
            return result + "}";
        }

        public string getOpenList()
        {
            string result = "{\"open\":[";
            string open = "";
            foreach (SerialPort port in openedList)
                open += "\"" + port.PortName + "\",";
            if (open.Length > 0)
                // delete last ,
                result += open.Substring(0, open.Length - 1);
            result += "],\"occupy\":[";
            string occupy = "";
            foreach (SerialPort port in portList)
            {
                if (openedList.Contains(port))
                    continue;
                bool canOpen = true;
                try
                {
                    port.BaudRate = 9600;
                    port.Open();
                    port.Close();
                }
                catch
                {
                    canOpen = false;
                }
                if (!canOpen)
                    occupy += "\"" + port.PortName + "\",";
            }
            if (occupy.Length > 0)
                // delete last ,
                result += occupy.Substring(0, occupy.Length - 1);
            return result + "]}";
        }

        public string openPort(string name, string baud)
        {
            foreach (SerialPort port in portList)
            {
                if (port.PortName == name)
                {
                    if (openedList.Contains(port))
                        return "{\"data\": \"port " + name + " already opened\"}";
                    try
                    {
                        port.BaudRate = int.Parse(baud);
                    }
                    catch
                    {
                        return "{\"data\": \"port " + name + " open error baud rate error\"}";
                    }
                    port.DataReceived += DataReceivedHandler;
                    port.Open();
                    openedList.Add(port);
                    return "{\"data\": \"port " + name + " open success\"}";
                }
            }
            return "{\"data\": \"not found port " + name + " open error\"}";
        }

        private static void DataReceivedHandler(object sender, SerialDataReceivedEventArgs e)
        {
            SerialPort sp = (SerialPort)sender;
            string indata = sp.ReadExisting();
        }

        public string closePort(string name)
        {
            foreach (SerialPort port in openedList)
            {
                if (port.PortName == name)
                {
                    port.Close();
                    openedList.Remove(port);
                    return "{\"data\": \"port " + name + " close ok\"}";
                }
            }
            return "{\"data\": \"port " + name + " not opened can not be close\"}";
        }

        public void closeAllPort()
        {
            foreach(SerialPort port in openedList)
                port.Close();
            openedList.Clear();
        }
    }
}
