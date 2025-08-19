!mod$ v1 sum:18c0721cbb1a9af3
!need$ ae09dad6df637892 n cg_data
module tinfo
use cg_data,only:kz
integer(4),parameter::max_threads=1024_4
integer(4)::last_n(0_8:1024_8)
integer(4)::myid
!$omp threadprivate(myid)
integer(4)::num_threads
!$omp threadprivate(num_threads)
integer(4)::ilow
!$omp threadprivate(ilow)
integer(4)::ihigh
!$omp threadprivate(ihigh)
end
