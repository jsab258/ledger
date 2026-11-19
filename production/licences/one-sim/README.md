# One simulation in the browser: licence texts read from the PC (19 Nov 2026, 17:00)

Advisor 250 (his yes 16:18) approved two lines on condition that wasi-libc's and the compiler's helper routines' full licence texts are read first. Read in full here on 19 Nov 2026 from:
- https://raw.githubusercontent.com/WebAssembly/wasi-libc/2e6fb9d8ee0c/LICENSE (and LICENSE-MIT, LICENSE-APACHE, LICENSE-APACHE-LLVM): commit 2e6fb9d8ee0c is the one wasi-sdk 34's VERSION file names.
- https://raw.githubusercontent.com/llvm/llvm-project/main/compiler-rt/LICENSE.TXT

What they say, against the study (production/research/lane/ONE-SIM-METHOD-2026-11-19.md on the lane branch):
- wasi-libc: Apache 2.0 with LLVM Exceptions, Apache 2.0 and MIT, as the study says, BUT portions come from third-party works under their own licences: dlmalloc (CC0), emmalloc (MIT), cloudlibc (BSD-2-Clause), musl (MIT), musl-fts (BSD-3-Clause). The study and line (a) name none of BSD-2, BSD-3 or CC0.
- compiler-rt: Apache 2.0 with LLVM Exceptions, plus the legacy dual licence (University of Illinois/NCSA or MIT) for older code. The study had it unread; line (a) names neither the legacy NCSA text.

All are permissive and keep-the-notice licences, but the texts are not what the study says, so per advisor 250 line (a) is HELD and reported; line (b) (tools never shipped) is added to the allowlist as item 17.
Proposed rewording of line (a) for his yes: "The browser prototype only: the pieces of the LLVM project's C++ library and helper routines and of wasi-libc that the compiler builds into the simulation file (Apache 2.0 with the LLVM exception, Apache 2.0, MIT; with portions under BSD-2-Clause, BSD-3-Clause, CC0 and the University of Illinois/NCSA licence), notices kept."
