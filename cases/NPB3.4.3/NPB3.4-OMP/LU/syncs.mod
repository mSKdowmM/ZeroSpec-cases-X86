!mod$ v1 sum:e3697dde0b3b9f0e
!need$ 86ffa13fb8cd4967 n lu_data
module syncs
use lu_data,only:isiz2
integer(4),parameter::padim=16_4
integer(4)::isync(1_8:16_8,0_8:162_8)
integer(4)::mthreadnum
!$omp threadprivate(mthreadnum)
integer(4)::iam
!$omp threadprivate(iam)
end
