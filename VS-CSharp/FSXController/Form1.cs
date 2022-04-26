using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

using System.Diagnostics;
using Microsoft.FlightSimulator.SimConnect;
using System.Runtime.InteropServices;
using NetMQ;
using NetMQ.Sockets;

namespace FSXLSTM
{
    
    public partial class Form1 : Form
    {

        //Args
        public int TARGET_ALTITUDE = 11000; //Altitude in feets
        
        public enum NN
        {
            LSTM,
            ANN
        };
        
        public NN NN_TYPE = NN.ANN; // Neural network used
        
        
        // Program variables
        private Stopwatch sw = new Stopwatch();
        private bool simrunning = false;

        private double x = 0;
        private double y = 0;
        private double z = 0;
        
        private double time = 0;
        
        List<double> altitude_ground_v = new List<double>();
        List<double> altitude_v = new List<double>();
        List<double> aoa_v = new List<double>();

        List<double> vx_v = new List<double>();
        List<double> vy_v = new List<double>();
        List<double> vz_v = new List<double>();

        List<double> vwx_v = new List<double>();
        List<double> vwy_v = new List<double>();
        List<double> vwz_v = new List<double>();

        List<double> vrx_v = new List<double>();
        List<double> vry_v = new List<double>();
        List<double> vrz_v = new List<double>();

        List<double> wvbx_v = new List<double>();
        List<double> wvby_v = new List<double>();
        List<double> wvbz_v = new List<double>();

        List<double> wvwx_v = new List<double>();
        List<double> wvwy_v = new List<double>();
        List<double> wvwz_v = new List<double>();

        List<double> ax_v = new List<double>();
        List<double> ay_v = new List<double>();
        List<double> az_v = new List<double>();

        List<double> cosine_v = new List<double>();
        List<double> sine_v = new List<double>();

        List<double> pitch_v = new List<double>();
        List<double> bank_v = new List<double>();
        List<double> heading_v = new List<double>();

        List<double> rudder_v = new List<double>();
        List<double> elevator_v = new List<double>();
        List<double> aileron_v = new List<double>();

        List<double> eng_rpm_v = new List<double>();
        List<double> throttle_v = new List<double>();

        List<double> time_v = new List<double>();

        List<double> x_v = new List<double>();
        List<double> y_v = new List<double>();
        List<double> z_v = new List<double>();
        
        
        enum DEFINITIONS
        {
            Control1,
            Surfaces
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

        private int current = 0;
        private int iterations = 0;
        
        // this is how you declare a data structure so that
        // simconnect knows how to fill it/read it.
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Control1
        {
            public double altitude_ground { get; set; }
            public double altitude { get; set; }

            public double aoa { get; set; }

            // velocity body
            public double vx { get; set; }
            public double vy { get; set; }
            public double vz { get; set; }

            // velocity world 
            public double vwx { get; set; }
            public double vwy { get; set; }
            public double vwz { get; set; }

            // Velocity rotation
            public double vrx { get; set; }
            public double vry { get; set; }
            public double vrz { get; set; }

            // wind velocity body
            public double wvbx { get; set; }
            public double wvby { get; set; }
            public double wvbz { get; set; }

            // wind velocity world
            public double wvwx { get; set; }
            public double wvwy { get; set; }
            public double wvwz { get; set; }

            // Acceleration
            public double ax { get; set; }
            public double ay { get; set; }
            public double az { get; set; }

            // rotation
            public double pitch { get; set; }
            public double bank { get; set; }
            public double heading { get; set; }

            // Control Surfaces
            public double rudder { get; set; }
            public double elevator { get; set; }
            public double aileron { get; set; }

            // Engines
            public double eng_rpm { get; set; }
            public double throttle { get; set; }

            // time
            public double time { get; set; }
        }
        
        // this is how you declare a data structure so that
        // simconnect knows how to fill it/read it.
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 1)]
        struct Surfaces
        {
            // Control Surfaces
            public double elevator { get; set; }
            public double aileron { get; set; }
            
            public double throttle_1 { get; set; }
            
            public double throttle_2 { get; set; }
        }


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
            client.Connect("tcp://localhost:5555");
            
            Console.WriteLine("Connected");

            try
            {
                
                
                simconnect = new SimConnect("Managed Data Request",  this.Handle, WM_USER_SIMCONNECT, null, 0);
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
                simconnect.AddToDataDefinition(DEFINITIONS.Surfaces, "ELEVATOR POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Surfaces, "AILERON POSITION", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                simconnect.AddToDataDefinition(DEFINITIONS.Surfaces, "General Eng Throttle Lever Position:1", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);
                simconnect.AddToDataDefinition(DEFINITIONS.Surfaces, "General Eng Throttle Lever Position:2", "", SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                
                // IMPORTANT: register it with the simconnect managed wrapper marshaller
                // if you skip this step, you will only receive a uint in the .dwData field.
                simconnect.RegisterDataDefineStruct<Control1>(DEFINITIONS.Control1);
                simconnect.RegisterDataDefineStruct<Surfaces>(DEFINITIONS.Surfaces);
                
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
                        sw.Start();
                        simrunning = true;
                    }

                    
                    double dt = sw.ElapsedMilliseconds;
                    time += dt;
                    sw.Restart();

                    if (current > 0)
                    {
                        x += vwx_v.Last() * dt / 1000.0;
                        y += vwy_v.Last() * dt / 1000.0;
                        z += vwz_v.Last() * dt / 1000.0;
                    }
                    
                    Control1 s1 = (Control1) data.dwData[0];

                    altitude_ground_v.Add(s1.altitude_ground);
                    altitude_v.Add(s1.altitude);

                    aoa_v.Add(s1.aoa);

                    vx_v.Add(s1.vx);
                    vy_v.Add(s1.vy);
                    vz_v.Add(s1.vz);

                    vwx_v.Add(s1.vwx);
                    vwy_v.Add(s1.vwy);
                    vwz_v.Add(s1.vwz);

                    vrx_v.Add(s1.vrx);
                    vry_v.Add(s1.vry);
                    vrz_v.Add(s1.vrz);

                    wvbx_v.Add(s1.wvbx);
                    wvby_v.Add(s1.wvby);
                    wvbz_v.Add(s1.wvbz);

                    wvwx_v.Add(s1.wvwx);
                    wvwy_v.Add(s1.wvwy);
                    wvwz_v.Add(s1.wvwz);

                    ax_v.Add(s1.ax);
                    ay_v.Add(s1.ay);
                    az_v.Add(s1.az);

                    cosine_v.Add(Math.Cos(s1.pitch));
                    sine_v.Add(Math.Sin(s1.pitch));

                    pitch_v.Add(s1.pitch);
                    bank_v.Add(s1.bank);
                    heading_v.Add(s1.heading);

                    rudder_v.Add(s1.rudder);
                    elevator_v.Add(s1.elevator);
                    aileron_v.Add(s1.aileron);

                    eng_rpm_v.Add(s1.eng_rpm);
                    throttle_v.Add(s1.throttle);

                    time_v.Add(s1.time);

                    x_v.Add(x);
                    y_v.Add(y);
                    z_v.Add(z);
                    
                    current++;
                    //Console.WriteLine("Dt {0}", dt);
                    //Console.WriteLine("Current {0}", current);

                    Tuple<double[], double[]> tuple;
                        
                    if (NN_TYPE == NN.LSTM)
                    {

                        int window = 15;

                        if (current < window)
                        {
                            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1,
                                SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.ONCE, 0, 0, 0, 0);
                            return;
                        }

                        tuple = LSTM_data_process(window);
                    }

                    else
                    {
                        tuple = ANN_data_process();
                    }

                    send(s1, tuple.Item1, tuple.Item2);
                    break;

                default:
                    break;
            }
        }

        Tuple<double[], double[]> LSTM_data_process(int window)
        {

            int n_elems_e = 6;
            int n_elems_a = 5;
            double[] Xe = new double[window * n_elems_e];
            double[] Xa = new double[window * n_elems_a];

            int s = vrx_v.Count - window;
            
            for (int i = 0; i < window; i++)
            {
                Xe[i * n_elems_e + 0] = aoa_v[s + i];
                Xe[i * n_elems_e + 1] = pitch_v[s + i];
                Xe[i * n_elems_e + 2] = bank_v[s + i];
                Xe[i * n_elems_e + 3] = vwy_v[s + i];
                Xe[i * n_elems_e + 4] = vz_v[s + i];
                Xe[i * n_elems_e + 5] = TARGET_ALTITUDE - altitude_v[s + i];

                Xa[i * n_elems_a + 0] = aoa_v[s + i];
                Xa[i * n_elems_a + 1] = pitch_v[s + i];
                Xa[i * n_elems_a + 2] = bank_v[s + i];
                Xa[i * n_elems_a + 3] = elevator_v[s + i];
                Xa[i * n_elems_a + 4] = vry_v[s + i];
                //Xa[i * n_elems_e + 5] = TARGET_ALTITUDE - altitude_v[s + i];
            }

            return Tuple.Create(Xe,Xa);
        }
        
        
        Tuple<double[], double[]> ANN_data_process()
        {
            double da = TARGET_ALTITUDE - altitude_v.Last();
            
            double[] Xe = new double[] {aoa_v.Last(), pitch_v.Last(),
                bank_v.Last(), vwy_v.Last(), vz_v.Last(), da};
                    
            double[] Xa = new double[] {aoa_v.Last(), elevator_v.Last(), pitch_v.Last(), bank_v.Last(), vry_v.Last(), da};

            return Tuple.Create(Xe,Xa);
        }
        
        byte[] GetBytesBlock(double[] values)
        {
            var result = new byte[values.Length * sizeof(double)];
            Buffer.BlockCopy(values, 0, result, 0, result.Length);
            return result;
        }


        void send(Control1 s1, double[] Xe, double[] Xa)
        {

            byte[] Xes = GetBytesBlock(Xe);
            byte[] Xas = GetBytesBlock(Xa);
            byte[][] X = new[] {Xes, Xas};
            client.SendMultipartBytes(X);


            List<byte[]> msg = client.ReceiveMultipartBytes();
            
            
            float elevator = BitConverter.ToSingle(msg[0],0);
            float aileron = BitConverter.ToSingle(msg[1],0);
            //float throttle = BitConverter.ToSingle(msg[2],0);

            Console.WriteLine("E: {0}", elevator);
            Console.WriteLine("A: {0}", aileron);
            //Console.WriteLine("T: {0}\n", throttle);
            
            var surfaces = new Surfaces();
            surfaces.elevator = elevator;
            surfaces.aileron = aileron;
            surfaces.throttle_1 = 1.0;
            surfaces.throttle_2 = 1.0;
            simconnect.SetDataOnSimObject(DEFINITIONS.Surfaces, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_DATA_SET_FLAG.DEFAULT, surfaces);
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.ONCE, 0, 0, 0, 0);
        }

        private void buttonStart(object sender, EventArgs e)
        {
            if (simconnect == null)
            {
                connect();
            }
            
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.ONCE, 0, 0, 0, 0);
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            simconnect.RequestDataOnSimObject(DATA_REQUESTS.REQUEST_1, DEFINITIONS.Control1, SimConnect.SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD.NEVER, 0, 0, 0, 0);
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

    }
}