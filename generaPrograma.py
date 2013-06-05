#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ok lpod 1.0
# Import from lpod
from lpod.document import odf_get_document
from lpod.document import odf_new_document
from lpod.paragraph import odf_create_paragraph

import  csv, sys, unidecode, re

def create_document():
    my_document = odf_new_document('text')
    style_filename = "estils/estils_programa.odt"
    style_document = odf_get_document(style_filename)
    my_document.delete_styles()
    my_document.merge_styles_from(style_document)
    return my_document

def save_document(my_document,outfilepath,tipus_actual,dia_actual,hora_actual):
    base_outfilepath = outfilepath[0:outfilepath.find('.odt')]
    outfilepath = base_outfilepath + '__' + slugify(tipus_actual)  + '_dia' + dia_actual + '_' + slugify(hora_actual) + '.odt'
    my_document.save(target=outfilepath, pretty=True)
    print "New file generated %s" % outfilepath


def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)


def main():
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: sys.argv[0] infilepath outfilepath')
        sys.exit(1)

    infilepath = sys.argv[1]
    outfilepath = sys.argv[2]

    tipus_actual = '-'
    dia_actual = '-'
    hora_actual = '-'

    DIAS = {
        '2': 'Martes, 2 de julio',
        '3': 'Miércoles, 3 de julio',
        '4': 'Jueves, 4 de julio',
        '5': 'Viernes, 5 de julio'
    }
    my_document = None
    body = None

    with open(infilepath, 'rb') as infile:
        aportacions = csv.DictReader(infile, delimiter=',')
        for aportacio in aportacions:
            tipologia = aportacio['Tipologia']
            if tipologia == 'Comunicació':
                tipologia = 'Comunicación'
            elif tipologia == 'Clip d\'aula':
                tipologia = 'Clip de aula'
            tipologia = tipologia.decode('utf-8')

            if tipologia != tipus_actual:
                if tipus_actual != '-':
                    save_document(my_document,outfilepath,tipus_actual,dia_actual,hora_actual)
                tipus_actual = tipologia
                dia_actual = '-'
                hora_actual = '-'

            if aportacio['Dia'].decode('utf-8') != dia_actual:
                if dia_actual != '-':
                    save_document(my_document,outfilepath,tipus_actual,dia_actual,hora_actual)
                dia_actual = aportacio['Dia'].decode('utf-8')
                hora_actual = '-'

            if aportacio['Hora'].decode('utf-8') != hora_actual:
                if hora_actual != '-':
                    save_document(my_document,outfilepath,tipus_actual,dia_actual,hora_actual)
                hora_actual = aportacio['Hora'].decode('utf-8')
                my_document = create_document()
                body = my_document.get_body()


            lloc = "%s. %s" % (aportacio['Edifici'].decode('utf-8'), aportacio['Aula'].decode('utf-8') )
            paragraph = odf_create_paragraph( lloc, style = 'lloc')
            body.append(paragraph)

            paragraph = odf_create_paragraph(aportacio['Títol'].decode('utf-8'), style = 'titolaportacio')
            body.append(paragraph)

            paragraph = odf_create_paragraph(aportacio['Autors'].decode('utf-8'), style = 'autors')
            body.append(paragraph)
            if aportacio['Afiliació'] != '':
                paragraph = odf_create_paragraph(aportacio['Afiliació'].decode('utf-8'), style = 'centretreball')
                body.append(paragraph)

            body.append(odf_create_paragraph(''))

            if len(aportacio['Observacions']) > 0:
                paragraph = odf_create_paragraph(aportacio['Observacions'].decode('utf-8'), style= 'observacions')
                body.append(paragraph)
                body.append(odf_create_paragraph(''))

            paragraph = odf_create_paragraph(aportacio['Resum'].decode('utf-8'), style= 'resum')
            body.append(paragraph)
            # paragraph = odf_create_paragraph('Palabras clave: ' + aportacio['Paraules clau'].decode('utf-8'), style= 'keywords')
            # body.append(paragraph)

            paragraph = odf_create_paragraph(u'Nucleos temáticos:', style='titolnuclis')
            body.append(paragraph)

            nuclis = []
            for nucli in [aportacio['Nucli temàtic 1'],aportacio['Nucli temàtic 2']]:
                if nucli.strip() != '':
                    if nucli == 'I. Infantil i Primària: aquí comença tot':
                        nucli = 'I. Infantil y Primaria: ahí empieza todo'
                    if nucli =='II. Didàctica i formació del professorat':
                        nucli ='II. Didáctica y formación del profesorado'
                    if nucli =='III. Modelització i formalització':
                        nucli ='III. Modelización y formalización'
                    if nucli =='IV. Resolució de problemes':
                        nucli ='IV. Resolución de problemas'
                    if nucli =='V. Materials i recursos a l’aula de matemàtiques':
                        nucli ='V. Materiales y recursos en el aula de matemáticas'
                    if nucli =='VI. Connexions i contextos':
                        nucli ='VI. Conexiones y contextos'
                    if nucli =='VII. Comunicació i divulgació':
                        nucli = 'VII. Comunicación y divulgación'

                    nuclis.append(nucli.decode('utf-8'))


            if len(nuclis) > 0:
                for nucli in nuclis:
                    body.append(odf_create_paragraph(nucli, style='nuclis'))
            else:
                print 'Comunicacio %s - %s no te cap nucli tematic' % (aportacio['Codi'], aportacio['Títol'])

            body.append(odf_create_paragraph(''))
            body.append(odf_create_paragraph(''))

    # Save the last document
    if my_document:
        save_document(my_document,outfilepath,tipus_actual,dia_actual,hora_actual)



if __name__ == '__main__':
    main()