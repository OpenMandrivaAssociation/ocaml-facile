Name:           ocaml-facile
Version:        1.1
Release:        %mkrel 2
Summary:        OCaml library for constraint programming
License:        LGPL
Group:          Development/Other
URL:            http://www.recherche.enac.fr/opti/facile/
Source0:        http://www.recherche.enac.fr/opti/facile/distrib/facile-%{version}.tar.gz
Source1:        http://www.recherche.enac.fr/opti/facile/distrib/facile-%{version}-man.pdf
Source2:        http://www.recherche.enac.fr/opti/facile/distrib/facile-%{version}-man.html.tar.gz
Source3:        META-facile.in
Patch0:         examples-Makefile-buildall.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml-findlib

%description
FaCiLe is a constraint programming library on integer and integer set finite
domains written in OCaml. It offers all usual facilities to create and
manipulate finite domain variables, arithmetic expressions and constraints
(possibly non-linear), built-in global constraints (difference, cardinality,
sorting etc.) and search and optimization goals. FaCiLe allows as well to build
easily user-defined constraints and goals (including recursive ones), making
pervasive use of OCaml higher-order functionals to provide a simple and flexible
interface for the user. As FaCiLe is an OCaml library and not "yet another
language", the user benefits from type inference and strong typing discipline,
high level of abstraction, modules and objects system, as well as native code
compilation efficiency, garbage collection and replay debugger, all features of
OCaml (among many others) that allow to prototype and experiment quickly:
modeling, data processing and interface are implemented with the same powerful
and efficient language.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains documentation for the library %{name}.

%prep
%setup -q -n facile-%{version}
%patch0 -p0
cp %{SOURCE1} ./
(mkdir manual && cd manual && tar xzf %{SOURCE2})
sed -e 's/@VERSION@/%{verison}/g' < %{SOURCE3} > META

%build
./configure
make
(cd src && mkdir -p doc && \
 ocamldoc -d doc -html \
   fcl_genesis.mli fcl_debug.mli fcl_misc.mli fcl_float.mli fcl_stak.mli \
   fcl_domain.mli fcl_setDomain.mli fcl_data.mli fcl_cstr.mli fcl_var.mli \
   fcl_reify.mli fcl_invariant.mli fcl_boolean.mli fcl_alldiff.mli fcl_linear.mli \
   fcl_nonlinear.mli fcl_expr.mli fcl_arith.mli fcl_interval.mli fcl_gcc.mli \
   fcl_fdArray.mli fcl_conjunto.mli fcl_sorting.mli fcl_goals.mli fcl_opti.mli facile.mli)

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR/facile
ocamlfind install facile META src/*.mli src/facile.{cmi,cma,cmxa,a}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%dir %{_libdir}/ocaml/facile
%{_libdir}/ocaml/facile/META
%{_libdir}/ocaml/facile/*.cma
%{_libdir}/ocaml/facile/*.cmi

%files devel
%defattr(-,root,root)
%{_libdir}/ocaml/facile/*.a
%{_libdir}/ocaml/facile/*.cmxa
%{_libdir}/ocaml/facile/*.mli

%files doc
%defattr(-,root,root)
%doc src/doc
%doc facile-%{version}-man.pdf
%doc manual

