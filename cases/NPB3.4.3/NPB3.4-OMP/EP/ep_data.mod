!mod$ v1 sum:f44b2bff736752ca
module ep_data
character(1_8,1),parameter::class="C"
integer(4),parameter::m=32_4
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
integer(4),parameter::mk=16_4
integer(4),parameter::mm=16_4
integer(4),parameter::nn=65536_4
integer(4),parameter::nk=65536_4
integer(4),parameter::nq=10_4
real(8),parameter::a=1.220703125e9_8
real(8),parameter::s=2.71828183e8_8
real(8)::x(1_8:131072_8)
!$omp threadprivate(x)
real(8)::qq(0_8:9_8)
!$omp threadprivate(qq)
real(8)::q(0_8:9_8)
integer(4),parameter::t_total=1_4
integer(4),parameter::t_gpairs=2_4
integer(4),parameter::t_randn=3_4
integer(4),parameter::t_rcomm=4_4
integer(4),parameter::t_last=4_4
end
