#!/bin/bash
#SBATCH --job-name=HELLO_C
#SBATCH --output=HELLO_C.txt
#SBATCH --mem-per-cpu=1024
#SBATCH --partition=compute
#SBATCH --nodes=2

. /etc/profile.d/modules.sh

module load openmpi/2.1.2
module load python/3/mpi4py/3.0.0

export MPI_HOME=/opt/openmpi-2.1.2
export PATH=${MPI_HOME}/bin:${PATH}

g++ -o hello hello.c -I /opt/openmpi-2.1.2/include -L /opt/openmpi-2.1.2/lib -l mpi
mpirun ./hello
