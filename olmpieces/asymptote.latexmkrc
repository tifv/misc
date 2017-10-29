# latexmkrc regarding external Asymptote files
sub asy {
    my ($figurename, $figuredir) = fileparse($_[0]);
    pushd($figuredir);
    my $return = system("asy -f '$asyformat' '$figurename'");
    popd();
    return $return;
}
sub asy_eps { local $asyformat="eps"; return asy($_[0]); }
sub asy_pdf { local $asyformat="pdf"; return asy($_[0]); }
add_cus_dep("asy", "eps", 0, "asy_eps");
add_cus_dep("asy", "pdf", 0, "asy_pdf");

# vim: set ft=perl :#
