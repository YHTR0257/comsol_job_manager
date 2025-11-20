# COMSOL API Guide

```plaintext
COMSOL Command Line Interface Guide

# compile options


Compile options when compiling a COMSOL Model Java file:

   -classpathadd <classpath>    Additional classpath

Options when compiling an application using the COMSOL Compiler:

   -outputdir <path>            Specifies where the compiled application    
                                should be saved. Default is the directory   
                                where the mph file is located.
   -runtimetype {download}|     Type of runtime to include when compiling.  
     embed
   -platforms windows,linux,    The platforms to compile for. Specify as    
     macos,macosarm64           a comma separated list. Default is the      
                                platform where the compiler is run.
   -iconwindows <path>          Path to image file for icon on Windows.     
   -iconmacos <path>            Path to image file for icon on macOS.       
   -splash <path>               Path to image file for splash screen.       
   -phbarchive <path>           Path to an external physics archive,        
                                 (folder or .jar file).

   Options not given are taken from the application's Compiler node,        
   except for -outputdir and -platforms.

Example:

   comsolcompile file.java
   comsolcompile application.mph
   comsolcompile C:\Users\user\archive1 C:\Users\user\archive2

# batch options
Usage: <command> [options] [target] [target arguments]  
      
COMSOL commands:

   comsol                       Run COMSOL Multiphysics Desktop
   comsolbatch                  Run a COMSOL job
   comsolcluster                Run COMSOL on a cluster
   comsolclusterbatch           Run a COMSOL job on a cluster
   comsolclustermphserver       Run COMSOL Multiphysics Server on a cluster 
   comsolclusterxpl             Run COMSOL on a cluster
   comsolcompile                Compile a model file for Java or compile an 
                                  application into an executable application
                                  (the latter option requires COMSOL Compiler)
   comsolmphclient              Run COMSOL Multiphysics Desktop client      
   comsolmphserver              Run COMSOL Multiphysics Server
   comsolmphserver matlab       Run MATLAB with COMSOL Multiphysics Server  
   comsolpowerpointbatch        Update images in PowerPoint presentations   
   comsolxpl                    Run cross-platform COMSOL Desktop

COMSOL options:

   -3drend <{ogl}|dx9|sw>       3D renderer: OpenGL, DirectX or
                                  software rendering
   -alloc <{auto}|native|       Select from using the native memory allocator
            scalable>             or a scalable memory allocator
   -applicationsroot <path>     Specify custom path to the COMSOL Application
                                  Libraries root directory
   -autosave <{on}|off>         Control saving of recovery files
   -blas <{auto}|mkl|blas|      BLAS library to use
           aocl|path>
   -blaspath <path>             Set path to BLAS library
   -c <path>                    Path to license file
   -ckl                         Use class-kit license
   -comsolinifile <path>        Path to .ini-file to use when launching     
                                COMSOL
   -configuration <path>        Path to directory for storing the state for 
                                  the GUI between sessions, and for performing
                                  different caching tasks
   -data <path>                 Path to data directory
   -docroot <path>              Specify custom path to the COMSOL documentation
                                  root directory
   -h, -help                    Show this help message
   -keeplicenses <on|{off}>     Keep checked out licenses throughout session   -mpmode <throughput|         Set multiprocessor mode
             turnaround|owner>
   -np <no. of cores|{auto}>    Set number of cores
   -numafirst <numa number>     Set first NUMA node to bind process to      
   -numasets <no. of sets>      Set number of NUMA nodes to optimize        
                                processor usage
   -prefsdir <path>             Path to preference directory
   -recoverydir <path>          Path to recovery directories
   -tmpdir <path>               Path to temporary directory
   -v, -version                 Show version information

Batch options:

   -alivetime <seconds>         The time between writing status on disc     
   -batchlog <log filename>     File to store log in
   -batchlogout                 Log to standard out when storing on file    
   -cancel                      Cancel another process that runs outputfile 
   -checklicense <filename>     Print license requirement for an mph file   
   -classpathadd <classpath>    Additional classpath
   -clearmesh                   Clear mesh before saving
   -clearsolution               Clear solution data before saving
   -client                      Run as client
   -continue                    Continue computation
   -createplots                 Create default plots when running
   -dev <filename>              Path to a JAR-file with additional classes  
                                to call from the batch class file
   -error <{on}|off>            Stop if an error occurs
   -external                    The external process target for an operation   -graphics                    Display graphics
   -host <hostname>             Connect to host <hostname>
   -inputfile <filename>        The input file name (.mph or .class)        
   -job <job name>              The batch job to run
   -jobfile <filename>          The name of the file that contains the list 
                                of input and output filenames
   -methodcall <methodcall tag> The method call to run
   -methodinputnames <names>    Comma separated list of names of inputs for 
                                the method call to run
   -methodinputvalues <values>  Comma separated list of input values for    
                                the method call to run
                                Arrays and 2D arrays are entered using      
                                curly braces, e.g., {1,2,3}
   -methodinputfile <filename>  A file with inputs to the method call to run                                Each line in the file should have the format                                <name>=<value>
   -mode <{batch}|desktop>      Ignore Batch and Cluster Computing settings 
                                or use them as desktop settings
   -norun                       Do not compute the model
   -nosave                      Do not save the resulting model
   -operation <progress|cancel| The operation to run on the batch job       
               stop|update|
               clear|rerun>
   -outputfile <filename>       The output file name (if not specified the  
                                input file name is used)
   -paramfile <filename>        Table file containing parameter names in    
                                the first row and parameter values
                                in the following rows
   -pindex <parameter indices>  Comma separated list of parameter indices   
   -plist <parameter values>    Comma separated list of parameter values    
   -pname <parameter name>      Comma separated list of parameter names     
   -port <port number>          Connect to port <port number>
   -recover                     Recover and continue computation
   -resethistory                Compact history before saving
   -stop <level>                Stop another process that runs outputfile   
   -stoptime <seconds>          The time the batch job is allowed to run    
                                before it is stopped
   -study <study name>          The study to compute
   -usebatchlic                 Use batch license (requires batch licenses) 

Example:

   comsolbatch -inputfile <path> -outputfile <path> -study std1
```

