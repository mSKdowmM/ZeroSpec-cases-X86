!mod$ v1 sum:c3027e3be8127f58
!need$ 10b9cb0ba6f88daa n sp_data
module work_lhs
use sp_data,only:problem_size
integer(4),parameter::imaxp=162_4
real(8)::lhs(1_8:5_8,0_8:162_8)
!$omp threadprivate(lhs)
real(8)::lhsp(1_8:5_8,0_8:162_8)
!$omp threadprivate(lhsp)
real(8)::lhsm(1_8:5_8,0_8:162_8)
!$omp threadprivate(lhsm)
real(8)::cv(0_8:161_8)
!$omp threadprivate(cv)
real(8)::rhov(0_8:161_8)
!$omp threadprivate(rhov)
end
