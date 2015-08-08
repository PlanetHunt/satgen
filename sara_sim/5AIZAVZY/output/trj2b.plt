#---</DRAMA/RE-ENTRY/trj2b.plt/1.2>------------------------<BF/HTG>-<05/2013>---
#_______________________________________________________________________________
#    ######   ####     ##             #####   #####     ##    #    #    ##      
#    #       #        #  #            #    #  #    #   #  #   ##  ##   #  #     
#    #####    ####   ######           #    #  #####   ######  # ## #  ######    
#    #            #  #    #           #    #  #    #  #    #  #    #  #    #    
# ___######__#####___#____#___________#####___#____#__#____#__#____#__#____#____
#           ESA DEBRIS RISK ASSESSMENT AND MITIGATION ANALYSIS TOOL
#
#-------------------------------------------------------------------------------
#                 ---- DRAMA ( Re-entry Analysis  V 1.2 ) ----               
#-------------------------------------------------------------------------------
#  trj2b.plt is a GNUplot command file which plots the trajectories of all      
#  objects surviving re-entry, the parent trajectory and the demise/impact      
#  altitudes of ALL objects, as computed by the DRAMA Re-entry Analysis.        
#-------------------------------------------------------------------------------
#  Run identifier  (max. 6 characters)
#
#  sara    
#
#-------------------------------------------------------------------------------
#  Comment lines (...); don't use the following characters:  ; !
#  DRAMA-2.0                                                                     
#  Re-Entry Survival and Risk Analysis                                           
#
#-------------------------------------------------------------------------------
set data style lines
set term png large enhanced font Vera 14 size 800,600
set output "trj2b.png"
set yrange [0:*]
set xlabel 'Time [s]'
set ylabel 'Altitude [km]'
set title 'Demise/Impact Altitudes of all Objects'
plot \
'trj.hst.001.+00' u 1:2 t 'Object 001', \
'trj.hst.002.+00' u 1:2 t 'Object 002', \
'trj.hst.003.+00' u 1:2 t 'Object 003', \
'trj.hst.004.+00' u 1:2 t 'Object 004', \
'trj.hst.005.+00' u 1:2 t 'Object 005', \
'trj.hst.006.+00' u 1:2 t 'Object 006', \
'trj.hst.007.+00' u 1:2 t 'Object 007', \
'trj.hst.008.+00' u 1:2 t 'Object 008', \
'trj.hst.009.+00' u 1:2 t 'Object 009', \
'trj.hst.010.+00' u 1:2 t 'Object 010', \
'trj.hst.011.+00' u 1:2 t 'Object 011', \
'trj.hst.012.+00' u 1:2 t 'Object 012', \
'trj.hst.013.+00' u 1:2 t 'Object 013', \
'trj.hst.014.+00' u 1:2 t 'Object 014', \
'trj.hst.015.+00' u 1:2 t 'Object 015', \
'trj.hst.016.+00' u 1:2 t 'Object 016', \
'trj.hst.017.+00' u 1:2 t 'Object 017', \
'trj.hst.018.+00' u 1:2 t 'Object 018', \
'trj.hst.019.+00' u 1:2 t 'Object 019', \
'trj.hst.020.+00' u 1:2 t 'Object 020', \
'trj.hst.021.+00' u 1:2 t 'Object 021', \
'trj.hst.022.+00' u 1:2 t 'Object 022', \
'trj.hst.023.+00' u 1:2 t 'Object 023', \
'trj.hst.024.+00' u 1:2 t 'Object 024', \
'trj.hst.025.+00' u 1:2 t 'Object 025', \
'trj.hst.026.+00' u 1:2 t 'Object 026', \
'trj.hst.027.+00' u 1:2 t 'Object 027', \
'trj.hst.028.+00' u 1:2 t 'Object 028', \
'trj.hst.029.+00' u 1:2 t 'Object 029', \
'trj.hst.030.+00' u 1:2 t 'Object 030', \
'trj.hst.031.+00' u 1:2 t 'Object 031', \
'trj.hst.032.+00' u 1:2 t 'Object 032', \
'trj.hst.033.+00' u 1:2 t 'Object 033', \
'trj.hst.034.+00' u 1:2 t 'Object 034', \
'reentry.stv' u 8:6 t 'Demise/Impact' w p ps 2
