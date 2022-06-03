using System;
using Microsoft.FlightSimulator.SimConnect;

namespace FSXLSTM
{
    public static class Utils
    {
        public static bool IsStable(double pitch, double bank)
        {
            var PitchLimit = new double[] { -0.3, 0.1 };
            var BankLimit = new double[] { -0.2, 0.2 };
            return pitch > PitchLimit[0] && pitch < PitchLimit[1] &&
                bank > BankLimit[0] && bank < BankLimit[1];
        }

        public static double Degrees2Radians(double degree)
        {
            return (degree * Math.PI / 180);
        }

        public static double Radians2Degrees(double radians)
        {
            return radians * 180 / Math.PI;
        }

        public static bool IsStraightFlight(string manoeuvre)
        {
            return manoeuvre.IndexOf("StraightFlight") != -1;
        }

        public static double latitudeComponent(double length, double heading)
        {
            return length * Math.Cos(heading);
        }

        public static double longitudeComponent(double length, double heading)
        {
            return length * Math.Sin(heading);
        }
        
        public static double addLatitudeMeters(double lat, double dist, double altitude)
        {
            double dlat = dist / altitude;
            return dlat + lat;
        }

        public static double addLongitudeMeters(double lon, double lat, double dist, double altitude)
        {
            double a = Math.Sin(dist / (altitude * 2));
            double dlon = Math.Asin(a / Math.Cos(lat)) * 2;
            return dlon + lon;
        }

        public static double[] calculateDestinationPosition(double startLatitude, double startLongitude, double altitude, double heading, double distance)
        {
            int LATITUDE = 0;
            int LONGITUDE = 1;
            double[] endPoint = new double[2];

            endPoint[LATITUDE] = Degrees2Radians(startLatitude);
            endPoint[LONGITUDE] = Degrees2Radians(startLongitude);

            double latComp = latitudeComponent(distance, heading);
            double lonComp = longitudeComponent(distance, heading);

            double earthRadius = (6378.135 - 21 * Math.Sin(endPoint[LATITUDE])) * 1000;
            double alt = earthRadius + altitude;
            double newLat = addLatitudeMeters(endPoint[LATITUDE], latComp, alt);
            double newLon = addLongitudeMeters(endPoint[LONGITUDE], endPoint[LATITUDE], lonComp, alt);
            endPoint[LATITUDE] = newLat;
            endPoint[LONGITUDE] = newLon;

            return endPoint;
        }
    }
}
