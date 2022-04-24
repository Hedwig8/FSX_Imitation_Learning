using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System;
using System.Diagnostics;
using System.Windows.Forms;
using Microsoft.FlightSimulator.SimConnect;
using System.Runtime.InteropServices;
using System.Globalization;
using System.IO;
using System.Timers;
using CsvHelper;
using Timer = System.Windows.Forms.Timer;

namespace FSXControl
{
    public partial class Form1 : Form
    {
        private List<Struct1> log = null;
        enum DEFINITIONS
        {
            Struct1,
            Control1
        }

        enum DATA_REQUESTS
        {
            REQUEST_1,
        };


        enum GROUP
        {
            ID_PRIORITY_STANDARD = 1900000000,
        };

        enum PAUSE_EVENTS
        {
            PAUSE = 0,
            UNPAUSE,
            GEAR_UP,
            GEAR_DOWN,
            THROTTLE_SET,
            THROTTLE_FULL
        };


        enum GROUPID
        {
            FLAG = 2000000000,
        };
        
        const int WM_USER_SIMCONNECT = 0x0402;
        



        // this is how you declare a data structure so that
        // simconnect knows how to fill it/read it.
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Struct1
        {
            public double altitude { get; set; }
            
            //Velocity
            public double velocity_body_x { get; set; }
            public double velocity_body_y { get; set; }
            public double velocity_body_z { get; set; }
            
            public double velocity_rot_body_x { get; set; }
            public double velocity_rot_body_y { get; set; }
            public double velocity_rot_body_z { get; set; }

            //Aceleration
            public double acceleration_body_x { get; set; }
            public double acceleration_body_y { get; set; }
            public double acceleration_body_z { get; set; }
            
            // Rotation
            public double pitch { get; set; }
            public double bank { get; set; }
            public double heading { get; set; }
            
            // Control Surfaces
            public double rudder { get; set; }
            public double elevator { get; set; }
            public double aileron { get; set; }
            public double flaps_handle_ind { get; set; }
            public double spoilers_handle_ind { get; set; }

            //Engines
            public double General_Eng_Rpm_1 { get; set; }
            public double General_Eng_Throttle_Lever_Position_1 { get; set; }
            
            //Current time
            public double time { get; set; }
        };

        
        // this is how you declare a data structure so that
        // simconnect knows how to fill it/read it.
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Control1
        {
            // Control Surfaces
            public double rudder { get; set; }
            public double elevator { get; set; }
            public double aileron { get; set; }
            public double flaps_handle_ind { get; set; }
            public double spoilers_handle_ind { get; set; }

            public double General_Eng_Throttle_Lever_Position_1 { get; set; }
            
            public double General_Eng_Throttle_Lever_Position_2 { get; set; }
        }


        // define the structure for the var you want to set
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct SetHdg
        {
            public double hdg;
        };

        
        SimConnect simconnect = null;


        public Form1()
        {
            InitializeComponent();
        }

        
        void connect()
        { 
            
            try
            {
                simconnect = new SimConnect("Managed Data Request",  this.Handle, WM_USER_SIMCONNECT, null, 0);
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.PAUSE, "PAUSE_ON");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.UNPAUSE, "PAUSE_OFF");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.GEAR_UP, "GEAR_UP");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.GEAR_DOWN, "GEAR_DOWN");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.THROTTLE_SET, "THROTTLE_SET");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.THROTTLE_FULL, "THROTTLE_FULL");
                
                
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "RUDDER POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ELEVATOR POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "AILERON POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "FLAPS HANDLE INDEX", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "SPOILERS HANDLE POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "General Eng Throttle Lever Position:1", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "General Eng Throttle Lever Position:2", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                // IMPORTANT: register it with the simconnect managed wrapper marshaller
                // if you skip this step, you will only receive a uint in the .dwData field.
                simconnect.RegisterDataDefineStruct<Control1>(DEFINITIONS.Control1);
                
                // catch a simobject data request
                simconnect.OnRecvSimobjectData += new SimConnect.RecvSimobjectDataEventHandler(simconnect_OnRecvSimobjectData);

            }
            catch (COMException ex)
            {
                Console.WriteLine(ex);
            }
        }

        void simconnect_OnRecvSimobjectData(SimConnect sender, SIMCONNECT_RECV_SIMOBJECT_DATA data)
        {
            

            switch ((DATA_REQUESTS) data.dwRequestID)
            {
                case DATA_REQUESTS.REQUEST_1:
                    Control1 s1 = (Control1) data.dwData[0];
                    send();
                    break;

                default:
                    break;
            }
        }
        
        void send()
        {
            Console.WriteLine(log.Count);
            if (log.Count > 0)
            {
                var state = log.First();
                var control = new Control1();
                control.aileron = state.aileron;
                control.elevator = state.elevator;
                control.flaps_handle_ind = state.flaps_handle_ind;
                control.spoilers_handle_ind = state.spoilers_handle_ind;
                control.rudder = state.rudder;
                control.General_Eng_Throttle_Lever_Position_1 = state.General_Eng_Throttle_Lever_Position_1;
                control.General_Eng_Throttle_Lever_Position_2 = state.General_Eng_Throttle_Lever_Position_1;
                simconnect.SetDataOnSimObject(DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, control);
                log.RemoveAt(0);
            }
        }

        private void buttonStart(object sender, EventArgs e)
        {
            if (simconnect == null)
            {
                connect();
            }
            
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.SIM_FRAME, 0, 0, 0, 0);
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.NEVER, 0, 0, 0, 0);
        }
        
        private void PopulateListBox(ListBox lsb, string Folder, string FileType)
        {
            DirectoryInfo dinfo = new DirectoryInfo(Folder);
            FileInfo[] Files = dinfo.GetFiles(FileType);
            foreach (FileInfo file in Files)
            {
                lsb.Items.Add(file.Name);
            }
        }
        
        
        protected override void DefWndProc(ref Message m)
        {
            if (m.Msg == WM_USER_SIMCONNECT)
            {
                if (simconnect != null)
                {
                    simconnect.ReceiveMessage();
                }
            }
            else
            {
                base.DefWndProc(ref m);
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            PopulateListBox(listBox1, @".", "*.csv");
        }
        
        private void OnTimerEvent(object sender, EventArgs e)

        {
            lbl_loaded.Text = "";
        }
        
        public void readFromFile(string filename)
        {
            using (var reader = new StreamReader(filename))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var records =  csv.GetRecords<Struct1>();
                log = records.ToList();
            }
        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            string filename = listBox1.Text;
            Console.WriteLine(filename);
            readFromFile(filename);
            lbl_loaded.Text = "Loaded!";
            Timer t = new Timer();
            t.Interval = 2000;
            t.Enabled = true;
            t.Tick += new System.EventHandler(OnTimerEvent);   
        }
    }
}