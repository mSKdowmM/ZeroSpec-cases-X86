!mod$ v1 sum:e3d2f81cf3ee9a83
module timers
real(8)::start(1_8:64_8)
!$omp threadprivate(start)
real(8)::elapsed(1_8:64_8)
!$omp threadprivate(elapsed)
procedure(real(8))::elapsed_time
end
