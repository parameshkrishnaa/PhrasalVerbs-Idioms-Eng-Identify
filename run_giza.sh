#cd GIZA++-v2
./GIZA++-v2/plain2snt.out $1 $2
#cd mkcls-v2
./mkcls-v2/mkcls -p$1 -V "${1}.classes"
./mkcls-v2/mkcls -p$2 -V "${2}.vcb.classes"
#cd GIZA++-v2
./GIZA++-v2/snt2cooc.out "${1}.vcb" "${2}.vcb" "${1}_${2}.snt" > "${1}_${2}.cooc"
./GIZA++-v2/GIZA++ -S "${1}.vcb" -T "${2}.vcb" -C "${1}_${2}.snt" -CoocurrenceFile "${1}_${2}.cooc" -o Result -outputpath out
