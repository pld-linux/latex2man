Summary:	Latex2man - translate UNIX manual pages written with LaTeX
Summary(pl.UTF-8):	Latex2man - tłumaczenie uniksowych stron podręcznika napisanych w LaTeXu
Name:		latex2man
Version:	1.26
Release:	2
License:	LaTeX Project Public License
Group:		Applications/Text
Source0:	http://mirror.ctan.org/support/%{name}.zip
# Source0-md5:	2b170c92f2e7a70fc29c7e53b8d6f459
URL:		ftp://tug.ctan.org/pub/tex-archive/help/Catalogue/entries/latex2man.html
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
Requires(post,postun):	/usr/bin/texhash
Requires:	perl-base
Requires:	texlive-latex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		texhash umask 022; [ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2;

%description
Latex2man is a tool to translate UNIX manual pages written with LaTeX
into a format understood by the UNIX man(1) command. Alternatively
HTML, TexInfo, or LaTeX code can be produced too.

%description -l pl.UTF-8
Latex2man to narzędzie do tłumaczenia uniksowych stron podręcznika
napisanych w LaTeXu do formatu rozumianego przez uniksowe polecenie
man(1). Alternatywnie może być tworzony kod HTML, TexInfo lub LaTeXa.

%prep
%setup -q -n %{name}

# disable install-info
%{__sed} -i -e '/install-info/d' Makefile
# remove bogus cleaning on every stage (removes some files to be installed)
%{__sed} -i -e '/\$(MAKE) clean/d;s/install: realclean all/install: all/' Makefile
# kill /usr/bin/env wrapper (and ensure perl shebang is left)
%{__sed} -i -e '1d' latex2man
grep -q '^#!/usr/bin/perl' latex2man

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_infodir},%{_docdir}/html,%{_datadir}/texmf/tex/latex/latex2man}

%{__make} install \
	BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir} \
	HTML_DIR=$RPM_BUILD_ROOT%{_docdir}/html \
	INFO_DIR=$RPM_BUILD_ROOT%{_infodir} \
	CFG_DIR=$RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/latex2man \
	TEX_DIR=$RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/latex2man

# keep just man format
%{__rm} $RPM_BUILD_ROOT%{_infodir}/{latex2man.info,dir} \
	$RPM_BUILD_ROOT%{_docdir}/html/latex2man.*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%texhash

%postun
%texhash

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/latex2man
%{_datadir}/texmf/tex/latex/latex2man
%{_mandir}/man1/latex2man.1*
