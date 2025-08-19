!mod$ v1 sum:3d9dbd2a964346fd
!need$ 01cdb080d72cc11d n bt_data
module work_lhs
use bt_data,only:problem_size
real(8)::fjac(1_8:5_8,1_8:5_8,0_8:162_8)
!$omp threadprivate(fjac)
real(8)::njac(1_8:5_8,1_8:5_8,0_8:162_8)
!$omp threadprivate(njac)
real(8)::lhs(1_8:5_8,1_8:5_8,1_8:3_8,0_8:162_8)
!$omp threadprivate(lhs)
end
