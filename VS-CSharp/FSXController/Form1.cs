using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

using Microsoft.FlightSimulator.SimConnect;
using System.Runtime.InteropServices;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;
using System.Text;
using System.Threading;

namespace FSXLSTM
{

    public partial class Form1 : Form
    {



        #region VARS
        //Args
        public string MANOEUVRE = "";
        public int TARGET_ALTITUDE = 0; //Altitude in feets
        public double INITIAL_HEADING = 0;
        public int TARGET_HEADING = 0;
        public int TARGET_MAX_ALTITUDE = 0;
        
        struct CommInput
        {
            public string Manoeuvre;
            public double TARGET_ALTITUDE;
            public double TARGET_HEADING;
            public double TARGET_MAX_ALTITUDE;

            public Control1[] Input;
        }

        struct CommOutput
        {
            public double elevator;
            public double aileron;
            public double rudder;
            public double throttle;
        }

        List<Control1> dataBuffer = new List<Control1>();
        bool AIControl = false;
        Thread ControlThread = null;
        
        #endregion

        #region PROGRAM_VARS
        // Program variables
        private bool simrunning = false;
        #endregion

        #region FSX_VARS
        enum DEFINITIONS
        {
            Control1,
            RudderSurface,
            AileronSurface,
            ThrottleSurface,
            ElevatorSurface
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
        #endregion

        #region DATA_FSX

        // this is how you declare a data structure so that
        // simconnect knows how to fill it/read it.
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Control1
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

            //Engines
            public double General_Eng_Rpm_1 { get; set; }
            public double General_Eng_Throttle_Lever_Position_1 { get; set; }



            //Current time

            public double time { get; set; }

        };


        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct ElevatorSurface
        {
            // Control Surfaces
            public double elevator { get; set; }
        }

        [StructLayout (LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct AileronSurface 
        { 
            // Control Surfaces
            public double aileron { get; set; }
        };

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct RudderSurface
        {
            // Control Surfaces
            public double rudder { get; set; }
        };

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct ThrottleSurface
        { 
            // Control Surfaces
            public double throttle { get; set; }
        };


        #endregion

        // define the structure for the var you want to set
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct SetHdg
        {
            public double hdg;
        };

        private RequestSocket client = null;
        SimConnect simconnect = null;

        public Form1()
        {
            InitializeComponent();
        }

        void connect()
        { 
            client = new RequestSocket();
            client.Connect("tcp://localhost:65432");
            
            Console.WriteLine("Connected");

            try
            {
                simconnect = new SimConnect("Managed Data Request",  this.Handle, WM_USER_SIMCONNECT, null, 1);
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.PAUSE, "PAUSE_ON");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.UNPAUSE, "PAUSE_OFF");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.GEAR_UP, "GEAR_UP");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.GEAR_DOWN, "GEAR_DOWN");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.THROTTLE_SET, "THROTTLE_SET");
                simconnect.MapClientEventToSimEvent(PAUSE_EVENTS.THROTTLE_FULL, "THROTTLE_FULL");

                // Control1
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "PLANE ALT ABOVE GROUND", "feet", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "Plane Altitude", "feet", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "INCIDENCE ALPHA", "Radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY WORLD X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY WORLD Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "VELOCITY WORLD Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ROTATION VELOCITY BODY X", "radians per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ROTATION VELOCITY BODY Y", "radians per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ROTATION VELOCITY BODY Z", "radians per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "RELATIVE WIND VELOCITY BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "RELATIVE WIND VELOCITY BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "RELATIVE WIND VELOCITY BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "AMBIENT WIND X", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "AMBIENT WIND Y", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "AMBIENT WIND Z", "Meters per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ACCELERATION BODY X", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ACCELERATION BODY Y", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ACCELERATION BODY Z", "feet per second", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "PLANE PITCH DEGREES", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "PLANE BANK DEGREES", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "PLANE HEADING DEGREES MAGNETIC", "radians", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "RUDDER POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ELEVATOR POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "AILERON POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "GENERAL ENG RPM:1", "rpm", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "General Eng Throttle Lever Position:1", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Control1, "ABSOLUTE TIME", "", SIMCONNECT_DATATYPE.FLOAT64, 0.0f, SimConnect.SIMCONNECT_UNUSED);

                // Surfaces
                simconnect.AddToDataDefinition(DEFINITIONS.ElevatorSurface, "ELEVATOR POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.AileronSurface, "AILERON POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.RudderSurface, "RUDDER POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.ThrottleSurface, "General Eng Throttle Lever Position:1", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                
                // IMPORTANT: register it with the simconnect managed wrapper marshaller
                // if you skip this step, you will only receive a uint in the .dwData field.
                simconnect.RegisterDataDefineStruct<Control1>(DEFINITIONS.Control1);
                simconnect.RegisterDataDefineStruct<ElevatorSurface>(DEFINITIONS.ElevatorSurface);
                simconnect.RegisterDataDefineStruct<AileronSurface>(DEFINITIONS.AileronSurface);
                simconnect.RegisterDataDefineStruct<RudderSurface>(DEFINITIONS.RudderSurface);
                simconnect.RegisterDataDefineStruct<ThrottleSurface>(DEFINITIONS.ThrottleSurface);

                // catch a simobject data request
                simconnect.OnRecvSimobjectData += new SimConnect.RecvSimobjectDataEventHandler(simconnect_OnRecvSimobjectData);
            }
            catch (COMException ex)
            {
                Console.WriteLine(ex);
            }
        }

            
        public List<T> getsublist<T>(List<T> data, int window)
        {
            return data.GetRange(data.Count - window, window);
        }
        
        void simconnect_OnRecvSimobjectData(SimConnect sender, SIMCONNECT_RECV_SIMOBJECT_DATA data)
        {
            switch ((DATA_REQUESTS) data.dwRequestID)
            {
                case DATA_REQUESTS.REQUEST_1:

                    if (!simrunning)
                    {
                        simrunning = true;
                    }

                    Control1 s1 = (Control1) data.dwData[0];
                    dataBuffer.Add(s1);

                    if (MANOEUVRE == "SteepCurve" && INITIAL_HEADING == 0)
                    {
                        INITIAL_HEADING = s1.heading;
                    }
                    
                    break;

                default:
                    break;
            }
        }

        CommInput? BuildCommInput()
        {
            if (dataBuffer.Count == 0) return null;
    
            CommInput CI = new CommInput()
            {
                Manoeuvre = MANOEUVRE,
                TARGET_ALTITUDE = TARGET_ALTITUDE,
                TARGET_HEADING = TARGET_HEADING,
                TARGET_MAX_ALTITUDE = TARGET_MAX_ALTITUDE,
                Input = dataBuffer.ToArray()
            };
            dataBuffer.Clear();
            return CI;
        }

        void GetControls()
        {
            while (AIControl)
            {
                CommInput? CI = BuildCommInput();
                if (CI != null)
                {
                    ControlFSX(SendInputReceiveOutput((CommInput)CI));
                } else {
                    Thread.Sleep(100);
                }
            }
        }

        CommOutput SendInputReceiveOutput(CommInput data)
        {
            client.SendMultipartBytes(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(data)));

            List<byte[]> msg = client.ReceiveMultipartBytes();

            string outputData = Encoding.UTF8.GetString(msg[0]);
            return JsonConvert.DeserializeObject<CommOutput>(outputData);

            //Console.WriteLine("E: {0}", commands.elevator);
            //Console.WriteLine("A: {0}", commands.aileron);
            //Console.WriteLine("T: {0}\n", throttle);
            
        }

        void ControlFSX(CommOutput controls)
        {
            if (controls.elevator < 10)
            {
                var elevator = new ElevatorSurface() { elevator = controls.elevator };
                simconnect.SetDataOnSimObject(DEFINITIONS.ElevatorSurface, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, elevator);
            }
            if (controls.aileron < 10)
            {
                var aileron = new AileronSurface() { aileron = controls.aileron };
                simconnect.SetDataOnSimObject(DEFINITIONS.AileronSurface, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, aileron);
            }
            if (controls.rudder < 10)
            {
                var rudder = new RudderSurface() { rudder = controls.rudder };
                simconnect.SetDataOnSimObject(DEFINITIONS.RudderSurface, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, rudder);
            }
            if (controls.throttle < 10)
            {
                var throttle = new ThrottleSurface() { throttle = controls.throttle };
                simconnect.SetDataOnSimObject(DEFINITIONS.ThrottleSurface, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, throttle);
            }
        }

        #region BUTTONS
        private void buttonStart(object sender, EventArgs e)
        {
            MANOEUVRE = this.Controls.OfType<RadioButton>().FirstOrDefault(r => r.Checked).Tag.ToString();
            switch (MANOEUVRE)
            {
                case "Approach":
                case "Climb":
                case "Immelmann":
                case "Split-S":
                    FormImmelmann formImmelmann = new FormImmelmann();
                    DialogResult dialogResult = formImmelmann.ShowDialog();
                    if (dialogResult == DialogResult.Yes)
                    {
                        var input = formImmelmann.Controls.OfType<TextBox>().Where(i => i.Tag.ToString() == "TARGET_ALTITUDE");
                        TARGET_ALTITUDE = int.Parse(input.ToList()[0].Text);
                    }

                    INITIAL_HEADING = 0; // to be initialized later when curve is called
                    break;
                case "HalfCubanEight":
                    FormHalfCubanEight formHalfCubanEight = new FormHalfCubanEight();
                    DialogResult dialogResultHalf = formHalfCubanEight.ShowDialog();
                    if (dialogResultHalf == DialogResult.Yes)
                    {
                        var input = formHalfCubanEight.Controls.OfType<TextBox>().Where(i => i.Tag.ToString() == "TARGET_ALTITUDE");
                        TARGET_ALTITUDE = int.Parse(input.ToList()[0].Text);
                        var input2 = formHalfCubanEight.Controls.OfType<TextBox>().Where(i => i.Tag.ToString() == "MAX_ALTITUDE");
                        TARGET_MAX_ALTITUDE = int.Parse(input2.ToList()[0].Text);
                    }

                    INITIAL_HEADING = 0; // to be initialized later when curve is called
                    break;
                case "SteepCurve":
                    FormHeading formHeading = new FormHeading();
                    DialogResult dialogResultHeading = formHeading.ShowDialog();
                    if (dialogResultHeading == DialogResult.Yes)
                    {
                        var input = formHeading.Controls.OfType<TextBox>().Where(i => i.Tag.ToString() == "TARGET_ALTITUDE");
                        TARGET_HEADING = int.Parse(input.ToList()[0].Text);
                    }
                    break;
                default:
                    break;
            }

            if (simconnect == null)
            {
                connect();
            }
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.SIM_FRAME, 0, 0, 0, 0);

            AIControl = true;
            ControlThread = new Thread(() => { GetControls(); });
            ControlThread.Start();
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            AIControl = false;
            ControlThread.Join();
            ControlThread = null;

            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.NEVER, 0, 0, 0, 0);
            simconnect.Dispose();
            simconnect = null;
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
            
        }
        #endregion
    }
}