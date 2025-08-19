!mod$ v1 sum:5eadbb4b5b38c12f
module ft_data
integer(4),parameter::nx=512_4
integer(4),parameter::ny=512_4
integer(4),parameter::nz=512_4
integer(4),parameter::maxdim=512_4
integer(4),parameter::niter_default=20_4
integer(4),parameter::kind2=4_4
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
integer(4),parameter::nxp=513_4
integer(4),parameter::ntotalp=134479872_4
real(8),parameter::nx_f=5.12e2_8
real(8),parameter::ntotal_f=1.34217728e8_8
intrinsic::dble
integer(4),parameter::fftblock_default=32_4
integer(4),parameter::fftblockpad_default=34_4
integer(4)::fftblock
integer(4)::fftblockpad
integer(4)::dims(1_8:3_8)
integer(4),parameter::t_total=1_4
integer(4),parameter::t_setup=2_4
integer(4),parameter::t_fft=3_4
integer(4),parameter::t_evolve=4_4
integer(4),parameter::t_checksum=5_4
integer(4),parameter::t_fftx=6_4
integer(4),parameter::t_ffty=7_4
integer(4),parameter::t_fftz=8_4
integer(4),parameter::t_max=8_4
logical(4)::timers_enabled
procedure(real(8))::timer_read
procedure(integer(4))::ilog2
procedure(real(8))::randlc
logical(4)::debug
logical(4)::debugsynch
real(8),parameter::seed=3.14159265e8_8
real(8),parameter::a=1.220703125e9_8
real(8),parameter::pi=3.141592653589793115997963468544185161590576171875_8
real(8),parameter::alpha=9.99999999999999954748111825886258685613938723690807819366455078125e-7_8
complex(8)::u(1_8:513_8)
complex(8)::sums(0_8:20_8)
integer(4)::niter
end
