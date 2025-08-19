!mod$ v1 sum:ae09dad6df637892
module cg_data
integer(4),parameter::na=150000_4
integer(4),parameter::nonzer=15_4
integer(4),parameter::niter=75_4
real(8),parameter::shift=1.1e2_8
real(8),parameter::rcond=1.000000000000000055511151231257827021181583404541015625e-1_8
integer(4),parameter::kz=4_4
logical(4),parameter::convertdouble=.false._4
character(11_8,1),parameter::compiletime="06 Aug 2025"
character(5_8,1),parameter::npbversion="3.4.3"
character(28_8,1),parameter::cs1="clang_wrapper.py --use-flang"
character(5_8,1),parameter::cs2="$(FC)"
character(6_8,1),parameter::cs3="(none)"
character(6_8,1),parameter::cs4="(none)"
character(12_8,1),parameter::cs5="-O3 -fopenmp"
character(9_8,1),parameter::cs6="$(FFLAGS)"
character(6_8,1),parameter::cs7="randi8"
integer(4),parameter::nz=38400000_4
integer(4),parameter::naz=2400000_4
intrinsic::int
integer(4),allocatable::colidx(:)
integer(4),allocatable::iv(:)
integer(4),allocatable::arow(:)
integer(4),allocatable::acol(:)
integer(4),allocatable::rowstr(:)
real(8),allocatable::v(:)
real(8),allocatable::aelt(:)
real(8),allocatable::a(:)
real(8),allocatable::x(:)
real(8),allocatable::z(:)
real(8),allocatable::p(:)
real(8),allocatable::q(:)
real(8),allocatable::r(:)
integer(4)::naa
integer(4)::firstrow
integer(4)::lastrow
integer(4)::firstcol
integer(4)::lastcol
integer(4)::nzz
real(8)::amult
!$omp threadprivate(amult)
real(8)::tran
!$omp threadprivate(tran)
procedure(real(8))::timer_read
integer(4),parameter::t_init=1_4
integer(4),parameter::t_bench=2_4
integer(4),parameter::t_conj_grad=3_4
integer(4),parameter::t_last=3_4
logical(4)::timeron
end
