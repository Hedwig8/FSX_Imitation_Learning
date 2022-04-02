using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;
using Microsoft.FlightSimulator.SimConnect;
using System.Runtime.InteropServices;
using System.Globalization;
using System.IO;
using System.Linq;
using CsvHelper;


namespace AircraftDataCollector
{
    public partial class Form1 : Form
    {

        #region Constants
        
        // User-defined win32 event
        const int WM_USER_SIMCONNECT = 0x0402;

        #endregion
        
        
        #region Vars


        private String subPath = "logs/";
        private List<Struct1> log = null;
        private List<Struct2> log2 = null;
        
        private bool simrunning = false;
        
        private Stopwatch sw = new Stopwatch();
        private Timer ConnectTimer = null;
        
        #endregion
        
        
        #region SimConnectVars
        
        SimConnect simconnect = null;
        
        enum EVENTS
        {
            SIMSTART,
            SIMSTOP,
            PAUSED,
            UNPAUSED
        };


        enum DEFINITIONS
        {
            Struct1,
            Struct2,
        }

        enum DATA_REQUESTS
        {
            REQUEST_1,
            REQUEST_2,
        };

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Struct1
        {
            
            public double altitude_abv_gnd { get; set; }
            public double altitude { get; set; }
            
            public double angle_of_attack { get; set; }
            
            //Velocity
            public double velocity_body_x { get; set; }
            public double velocity_body_y { get; set; }
            public double velocity_body_z { get; set; }
            
            
            public double velocity_world_x { get; set; }
            public double velocity_world_y { get; set; }
            public double velocity_world_z { get; set; }
            
            public double velocity_rot_body_x { get; set; }
            public double velocity_rot_body_y { get; set; }
            public double velocity_rot_body_z { get; set; }

            
            // Wind velocity
            public double wind_velocity_body_x { get; set; }
            public double wind_velocity_body_y { get; set; }
            public double wind_velocity_body_z { get; set; }
            
            public double wind_velocity_world_x { get; set; }
            public double wind_velocity_world_y { get; set; }
            public double wind_velocity_world_z { get; set; }
            
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
        struct Struct2
        {
            // this is how you declare a fixed size string
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)]
            private String _title;
            
            public String title
            {
                get {
                    return _title.ToString();
                }
                
                set {
                    this._title = value.ToString();
                }
            }
            
            public double ambient_density { get; set; }
            public double ambient_temperature { get; set; }
            public double ambient_pressure { get; set; }
            public double sea_level_pressure { get; set; }
            public double gear_position { get; set; }
            public double fuel_current { get; set; }
            public double precipitation_state { get; set; }
            public double time { get; set; }
        }

        #endregion


        #region Form
        public Form1()
        {
            System.IO.Directory.CreateDirectory(subPath);
            log = new List<Struct1>();
            log2 = new List<Struct2>();
            InitializeComponent();
            setButtons(false, false);
        }

        
        private void Form1_Load(object sender, EventArgs e)
        {
            ConnectTimer = new Timer();
            ConnectTimer.Interval = (1000); // 1s
            ConnectTimer.Tick += new EventHandler(ConnectTimer_Tick);
            ConnectTimer.Start();
        }
        
        private void ConnectTimer_Tick(object sender, EventArgs e)
        {
            textBox1.Text = "Trying to connect ...";
            if (openConnection())
            {
                ConnectTimer.Stop();
            }
        }
        
        // The case where the user closes the client
        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            closeConnection();
            GC.Collect();
        }
        
        #endregion
        
        
        #region Connection
        private bool openConnection()
        {
            if (simconnect == null)
            {
                try
                {
                    // the constructor is similar to SimConnect_Open in the native API
                    simconnect = new SimConnect("Managed Data Request", this.Handle, WM_USER_SIMCONNECT, null, 1);

                    setButtons(true, false);
                    
                    initDataRequest();

                    return true;
                }
                catch (COMException)
                {
                    return false;
                }
            }
            else
            {
                displayText("Error - try again");
                closeConnection();

                setButtons(false, false);
            }

            return false;
        }
        
        private void closeConnection()
        {
            if (simconnect != null)
            {
                // Unsubscribe from all the system events
                simconnect.UnsubscribeFromSystemEvent(EVENTS.SIMSTART);
                simconnect.UnsubscribeFromSystemEvent(EVENTS.SIMSTOP);
                
                // Dispose serves the same purpose as SimConnect_Close()
                simconnect.Dispose();
                simconnect = null;
            }
        }
        
        #endregion
        
        
        #region Buttons
        private void buttonStart_Click(object sender, EventArgs e)
        {
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Struct1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.SIM_FRAME, 0, 0, 0, 0);
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_2, DEFINITIONS.Struct2, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.SECOND, 0, 0, 0, 0);

            setButtons(false, true);
            
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Struct1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.NEVER, 0, 0, 0, 0);
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_2, DEFINITIONS.Struct2, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.NEVER, 0, 0, 0, 0);

            if (log.Count > 0 || log2.Count > 0)
            {
                SavePopup();
            }
            simrunning = false;
            sw.Reset();
            log.Clear();
            log2.Clear();
            resetText();
            setButtons(true, false);
        }
        
        public void SavePopup()
        {
            Form2 form2 = new Form2();
            string tag;

            DialogResult dialogresult_manoeuvre = form2.ShowDialog(this);
            // Show testDialog as a modal dialog and determine if DialogResult = OK.
            if (dialogresult_manoeuvre == DialogResult.Yes)
            {
                var checkedButton = form2.Controls.OfType<RadioButton>().FirstOrDefault(r => r.Checked);
                tag = checkedButton.Tag.ToString();
            }
            else
            {
                form2.Dispose();
                return;
            }
            
            form2.Dispose();

            // SECOND POPUP

            Form3 form3 = new Form3();
            string quality;

            DialogResult dialogresult_quality = form3.ShowDialog(this);

            if(dialogresult_quality == DialogResult.Yes)
            {
                var checkedButton = form3.Controls.OfType<RadioButton>().FirstOrDefault(r => r.Checked);
                quality = checkedButton.Tag.ToString();
                writeToCSV<Struct1>(log, quality, tag, "1");
                writeToCSV<Struct2>(log2, quality, tag, "2");
            }
            form3.Dispose();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            closeConnection();
            this.Close();
        }
        
        #endregion
        

        #region  SimConnect
        
        // Set up all the SimConnect related data definitions and event handlers
        private void initDataRequest()
        {
            try
            {
                // listen to connect and quit msgs
                simconnect.OnRecvOpen += new SimConnect.RecvOpenEventHandler(simconnect_OnRecvOpen);
                simconnect.OnRecvQuit += new SimConnect.RecvQuitEventHandler(simconnect_OnRecvQuit);

                // listen to exceptions
                simconnect.OnRecvException += new SimConnect.RecvExceptionEventHandler(simconnect_OnRecvException);

                // listen to events
                simconnect.OnRecvEvent += new SimConnect.RecvEventEventHandler(simconnect_OnRecvEvent);
                
                // Subscribe to system events
                simconnect.SubscribeToSystemEvent(EVENTS.SIMSTART, "SimStart");
                simconnect.SubscribeToSystemEvent(EVENTS.SIMSTOP, "SimStop");
                simconnect.SubscribeToSystemEvent(EVENTS.PAUSED, "Paused");
                simconnect.SubscribeToSystemEvent(EVENTS.UNPAUSED, "Unpaused");
                
                simconnect.SetSystemEventState(EVENTS.SIMSTART, SIMCONNECT_STATE.ON);
                simconnect.SetSystemEventState(EVENTS.SIMSTOP, SIMCONNECT_STATE.ON);
                simconnect.SetSystemEventState(EVENTS.PAUSED, SIMCONNECT_STATE.ON);
                simconnect.SetSystemEventState(EVENTS.UNPAUSED, SIMCONNECT_STATE.ON);
                
                
                // define a data structure
                
                // Struct 1
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "PLANE ALT ABOVE GROUND", "feet", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "Plane Altitude", "feet", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "INCIDENCE ALPHA", "Radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY WORLD X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY WORLD Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "VELOCITY WORLD Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ROTATION VELOCITY BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ROTATION VELOCITY BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ROTATION VELOCITY BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "RELATIVE WIND VELOCITY BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "RELATIVE WIND VELOCITY BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "RELATIVE WIND VELOCITY BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "AMBIENT WIND X", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "AMBIENT WIND Y", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "AMBIENT WIND Z", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ACCELERATION BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ACCELERATION BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ACCELERATION BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "PLANE PITCH DEGREES", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "PLANE BANK DEGREES", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "PLANE HEADING DEGREES MAGNETIC", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "RUDDER POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ELEVATOR POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "AILERON POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "FLAPS HANDLE INDEX", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "SPOILERS HANDLE POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "GENERAL ENG RPM:1", "rpm", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "General Eng Throttle Lever Position:1", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Struct1, "ABSOLUTE TIME", "", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                // Struct 2
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "title", null, SIMCONNECT_DATATYPE.STRING256, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "AMBIENT DENSITY", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "AMBIENT TEMPERATURE", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "AMBIENT PRESSURE", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "SEA LEVEL PRESSURE", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "GEAR POSITION", "enum", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "FUEL TOTAL QUANTITY WEIGHT", "Pounds", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Struct2, "AMBIENT PRECIP STATE", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                // IMPORTANT: register it with the simconnect managed wrapper marshaller
                // if you skip this step, you will only receive a uint in the .dwData field.
                simconnect.RegisterDataDefineStruct<Struct1>(DEFINITIONS.Struct1);
                simconnect.RegisterDataDefineStruct<Struct2>(DEFINITIONS.Struct2);


                // catch a simobject data request
                simconnect.OnRecvSimobjectData += new SimConnect.RecvSimobjectDataEventHandler(simconnect_OnRecvSimobjectData);

            }
            catch (COMException ex)
            {
                displayText(ex.Message);
            }
        }


        
        
        void displayStats(Struct1 s1)
        {
            resetText();
            
            
            displayText("Alt:       " + s1.altitude);
            displayText("AoA:       " + s1.angle_of_attack);
            
            displayText("\n");
            
            displayText("VelX:      " + s1.velocity_body_x);
            displayText("VelY:      " + s1.velocity_body_y);
            displayText("VelZ:      " + s1.velocity_body_z);
            
            displayText("\n");

            displayText("VelRX:     " + s1.velocity_rot_body_x);
            displayText("VelRY:     " + s1.velocity_rot_body_y);
            displayText("VelRZ:     " + s1.velocity_rot_body_z);
            
            displayText("\n");
            
            displayText("Pitch:     " + s1.pitch * 180 / Math.PI);
            displayText("Bank:      " + s1.bank * 180 / Math.PI);
            displayText("Heading:   " + s1.heading * 180 / Math.PI);
            
            displayText("\n");
            
            displayText("Rudder:    " + s1.rudder);
            displayText("Elevator:  " + s1.elevator);
            displayText("Aileron:   " + s1.aileron);
            displayText("Flaps:     " + s1.flaps_handle_ind);
            displayText("Spoilers:   " + s1.spoilers_handle_ind);
            
            displayText("\n");
            
            displayText("RPM:       " + s1.General_Eng_Rpm_1);
            displayText("Throttle   " + s1.General_Eng_Throttle_Lever_Position_1);
            
            displayText("\n");
        }
        
        void displayStats2(Struct2 s2)
        {
            resetText();
            
            displayText("Title: " + s2.title);
            displayText("Ambient density:" + s2. ambient_density);
            displayText("Ambient temperature: " + s2.ambient_temperature);
            displayText("Ambient pressure: " + s2.ambient_pressure);
            displayText("Sea level pressure: " + s2.sea_level_pressure);
            displayText("Gear position: " + s2.gear_position);
            displayText("Current fuel: " + s2.fuel_current);

            double avg = 0;
            double count = 0;
            
            for (int i = log2.Count - 1; i > 0 && i > log2.Count - 5; i--)
            {
                avg += log2[i - 1].fuel_current - log2[i].fuel_current;
                count++;
            }

            avg /= count;
            
            displayText("Calculated fuel flow: " + avg * 60 * 60);
            displayText("Minutes until out of fuel: " + (s2.fuel_current / (avg * 60)));
        }
        
        void simconnect_OnRecvSimobjectData(SimConnect sender, SIMCONNECT_RECV_SIMOBJECT_DATA data)
        {


            switch ((DATA_REQUESTS) data.dwRequestID)
            {
                case DATA_REQUESTS.REQUEST_1:
                    Struct1 s1 = (Struct1) data.dwData[0];
                    
                    if (!simrunning)
                    {
                        sw.Start();
                        simrunning = true;
                    }
                    
                    log.Add(s1);

                    if (log.Count % 100 == 0)
                    {
                        Struct1 current = log.Last();
                        displayStats(current);
                    }
                    break;

                case DATA_REQUESTS.REQUEST_2:
                    Struct2 s2 = (Struct2) data.dwData[0];
                    s2.time = log.Count == 0 ? 0 : log.Last().time;
                    log2.Add(s2);
                    break;
                
                default:
                    displayText("Unknown request ID: " + data.dwRequestID);
                    break;
            }
        }

        public bool paused = false;
        void simconnect_OnRecvEvent(SimConnect sender, SIMCONNECT_RECV_EVENT recEvent)
        {
            if(!simrunning)
                return;
            
            
            switch (recEvent.uEventID)
            {
                case (uint) EVENTS.SIMSTART:
                    if (!paused)
                    {
                        sw.Start();
                        displayText("Sim started");
                    }
                    break;

                case (uint) EVENTS.SIMSTOP:
                    if (!paused)
                    {
                        sw.Stop();
                        displayText("Sim stopped");
                    }
                    break;
                
                case (uint) EVENTS.PAUSED:
                    paused = true;
                    sw.Stop();
                    displayText("Sim stopped");
                    break;

                case (uint) EVENTS.UNPAUSED:
                    paused = false;
                    sw.Start();
                    displayText("Sim started");
                    break;
            }
        }
        
        
        void simconnect_OnRecvOpen(SimConnect sender, SIMCONNECT_RECV_OPEN data)
        {
            textBox1.Text = "Connected to FSX";
            textBox1.ForeColor = Color.Lime;
            setButtons(true, false);
        }

        
        // The case where the user closes FSX
        void simconnect_OnRecvQuit(SimConnect sender, SIMCONNECT_RECV data)
        {
            closeConnection();
            ConnectTimer.Start();
            textBox1.Text = "Trying to connect ...";
            textBox1.ForeColor = SystemColors.WindowText;
            setButtons(false, false);
        }

        
        void simconnect_OnRecvException(SimConnect sender, SIMCONNECT_RECV_EXCEPTION data)
        {
            displayText("Exception received: " + data.dwException);
        }

        #endregion
        
               
        #region File
        
        void writeToCSV<StructT>(List<StructT> logT, string quality, string id, string struct1or2)
        {
            string path = subPath + quality + "/" + id + "/";
            System.IO.Directory.CreateDirectory(path);

            string time = DateTime.Now.ToString("yyyy-MM-ddTHH-mm-ss");
            string filename = time + "_" + struct1or2 + ".csv";
            
            using (var writer = new StreamWriter(path + filename))
            using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
            {
                csv.WriteHeader<StructT>();
                csv.NextRecord();

                foreach (var s1 in logT)
                {
                    csv.WriteRecord<StructT>(s1);
                    csv.NextRecord();
                }
            }
        }

        #endregion
        
        
        #region Utils
        
        
        // Simconnect client will send a win32 message when there is 
        // a packet to process. ReceiveMessage must be called to
        // trigger the events. This model keeps simconnect processing on the main thread.

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
    
        
        private void setButtons(bool bStart, bool bStop)
        {
            buttonStart.Enabled = bStart;
            buttonStop.Enabled = bStop;
        }
        
        
        // Output text - display a maximum of 10 lines
        string output = "";

        void displayText(string s)
        {
            // remove first string from output
            output = output.Substring(output.IndexOf("\n") + 1);

            // add the new string
            output += "\n" + s;

            // display it
            richResponse.Text = output;
        }

        void resetText()
        {
            output = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
        }

        #endregion
        
    }
}
// End of sample
