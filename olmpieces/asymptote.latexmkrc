################################################################################
# Asymptote

sub asy {
    my ($asy_source_name, $asy_source_dir) = fileparse(shift);
    my $command = "asy -vv --offscreen";
    my $asy_format = shift;
    if (defined $asy_format)
        { $command .= " -f '$asy_format'"; }
    my $asy_latex = shift;
    if (defined $asy_latex)
        { $command .= " -tex '$asy_latex'"; }
    my $asy_latex_config = shift;
    if (defined $asy_latex_config && -e $asy_latex_config) {
        my ($asy_latex_config_name, $asy_config_dir) =
            fileparse($asy_latex_config);
        $asy_config_dir = File::Spec->catdir(Cwd->getcwd(), $asy_config_dir);
        $command .= " -dir '$asy_config_dir'";
        $command .= " -autoimport '$asy_latex_config_name'";
    }
    $command .= " '$asy_source_name'";
    pushd($asy_source_dir);
    #print $command, "\n";
    my $return = system($command);
    popd();
    return $return;
}
sub asy_eps {
    my $asy_source = shift;
    return asy_fmt($asy_source, "eps");
}
sub asy_pdf {
    my $asy_source = shift;
    return asy_fmt($asy_source, "pdf");
}
sub asy_fmt {
    my $asy_source = shift;
    my ($asy_sourcename, $asy_sourcedir) = fileparse($asy_source);
    if (
        $asy_sourcename =~ /$jobname-[0-9]+/ &&
        ( $asy_sourcedir eq "./" ||
            $out_dir ne "" && $asy_sourcedir eq $out_dir . "/" )
    ) {
        return asy($asy_source);
    }
    my $asy_format = shift;
    my $asy_latex_config = "figures/CONFIG_latex_fontenc.asy";
    if ($asy_format eq "eps") {
        return asy($asy_source, "eps", "latex", $asy_latex_config);
    }
    my $asy_latex = "pdflatex";
    if ($pdf_mode == 4) {
        $asy_latex = "lualatex";
        $asy_latex_config = "figures/CONFIG_latex_fontspec.asy";
    } elsif ($pdf_mode == 5) {
        $asy_latex = "xelatex";
        $asy_latex_config = "figures/CONFIG_latex_fontspec.asy";
    }
    return asy($asy_source, "pdf", $asy_latex, $asy_latex_config);
}
add_cus_dep("asy", "eps", 0, "asy_eps");
add_cus_dep("asy", "pdf", 0, "asy_pdf");

# vim: set ft=perl :############################################################
