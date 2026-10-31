using System;
using System.IO;
using System.Reflection;
using System.Web.Script.Serialization;

public static class SigmaBridge {
    public static int Main(string[] args) {
        try {
            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.InvariantCulture;
            System.Threading.Thread.CurrentThread.CurrentUICulture = System.Globalization.CultureInfo.InvariantCulture;
            string folder = Environment.GetEnvironmentVariable("SIGMASTUDIO_DIR");
            if (String.IsNullOrWhiteSpace(folder)) {
                string[] roots = {
                    Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                    Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86)
                };
                foreach (string root in roots) {
                    string candidate = Path.Combine(root, @"Analog Devices\SigmaStudio 4.7");
                    if (File.Exists(Path.Combine(candidate, "Analog.SigmaStudioServer.dll"))) {
                        folder = candidate;
                        break;
                    }
                }
            }
            if (String.IsNullOrWhiteSpace(folder) || !File.Exists(Path.Combine(folder, "Analog.SigmaStudioServer.dll")))
                throw new FileNotFoundException("Set SIGMASTUDIO_DIR to the installed SigmaStudio directory containing Analog.SigmaStudioServer.dll.");
            AppDomain.CurrentDomain.AssemblyResolve += delegate(object sender, ResolveEventArgs e) {
                string file = Path.Combine(folder, new AssemblyName(e.Name).Name + ".dll");
                return File.Exists(file) ? Assembly.LoadFrom(file) : null;
            };
            Assembly assembly = Assembly.LoadFrom(Path.Combine(folder, "Analog.SigmaStudioServer.dll"));
            if (args.Length == 0 || args[0] == "inspect") {
                foreach (Type type in assembly.GetExportedTypes()) {
                    Console.WriteLine(type.FullName);
                    foreach (MethodInfo method in type.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.DeclaredOnly))
                        Console.WriteLine(method.ToString());
                }
                return 0;
            }
            Type serverType = assembly.GetType("Analog.SigmaStudioServer.SigmaStudioServer", true);
            object server = Activator.CreateInstance(serverType);
            Console.WriteLine("CONNECTED " + serverType.FullName);
            if (args[0] == "sample") {
                int count=Int32.Parse(args[1]);
                int captureRegister=args.Length>2?Int32.Parse(args[2]):2074;
                if(captureRegister!=2074 && captureRegister!=2075)throw new ArgumentException("Capture register");
                if(count<1 || count>512) throw new ArgumentException("Sample count");
                double[] values=new double[count];
                MethodInfo read=serverType.GetMethod("REGISTER_READ_ARRAY");
                for(int j=0;j<count;j++) {
                    byte[] b=(byte[])read.Invoke(server,new object[]{"IC 1",captureRegister,3});
                    if(b.Length!=3)throw new Exception("Invalid read length");
                    int v=(b[0]<<16)|(b[1]<<8)|b[2];
                    if((v&0x800000)!=0)v-=0x1000000;
                    values[j]=v/524288.0;
                    System.Threading.Thread.Sleep(3);
                }
                Console.WriteLine(new JavaScriptSerializer().Serialize(values));return 0;
            }
            if (args[0] == "call") {
                var json = new JavaScriptSerializer();
                object[] call = json.Deserialize<object[]>(File.ReadAllText(args[2]));
                if(args[1]=="SET_OBJECT_PROPERTY") {
                    object[] vals = (object[])call[2];
                    if((string)call[0]=="setPosition") {
                        object[] xy=(object[])vals[0];
                        vals[0]=new System.Drawing.Point(Convert.ToInt32(xy[0]),Convert.ToInt32(xy[1]));
                    }
                    if(vals.Length==4 && (string)vals[2]=="Coefficients") {
                        object[] source = (object[])vals[3];
                        double[] dest = new double[source.Length];
                        for(int j=0;j<source.Length;j++) dest[j]=Convert.ToDouble(source[j]);
                        vals[3]=dest;
                    }
                }
                MethodInfo target = serverType.GetMethod(args[1]);
                ParameterInfo[] pars = target.GetParameters();
                for (int i=0; i<call.Length; i++) {
                    Type t = pars[i].ParameterType;
                    if (t.IsByRef || call[i] == null || t == typeof(object[])) continue;
                    call[i] = Convert.ChangeType(call[i], t);
                }
                object result = target.Invoke(server, call);
                Console.WriteLine(json.Serialize(new { result=result, arguments=call }));
                return 0;
            }
            if (args[0] == "probe") {
                MethodInfo method = serverType.GetMethod("GET_OBJECT_PROPERTY");
                object[] call = new object[] { "getControlValue", "DC2_2", null, new object[] { 0, 0, "DCValue" } };
                object result = method.Invoke(server, call);
                Console.WriteLine(new JavaScriptSerializer().Serialize(new { ok = result, values = call[2] }));
                return 0;
            }
            throw new ArgumentException("Unsupported command");
        } catch (Exception e) {
            Console.Error.WriteLine(e.ToString());
            return 1;
        }
    }
}
