// static/js/scripts.js

$(document).ready(function() {
    $('#classe_codigo').change(function() {
        var selectedClasse = $(this).val();
        if (selectedClasse) {
            // Fazer uma requisição AJAX para obter os assuntos
            $.ajax({
                url: '/get_assuntos/' + encodeURIComponent(selectedClasse),
                type: 'GET',
                success: function(data) {
                    var assuntoSelect = $('#assunto_codigo');
                    assuntoSelect.empty();
                    assuntoSelect.append('<option value="">Selecione um Assunto Processual</option>');
                    
                    // Iterar sobre os assuntos recebidos e adicioná-los ao select
                    $.each(data, function(ramo, subramos) {
                        assuntoSelect.append('<optgroup label="' + ramo + '">');
                        $.each(subramos, function(subramo, assuntos_nivel) {
                            assuntoSelect.append('<optgroup label="&nbsp;&nbsp;' + subramo + '">');
                            $.each(assuntos_nivel, function(assunto, detalhes) {
                                assuntoSelect.append('<option value="' + assunto + '">' + assunto + '</option>');
                            });
                            assuntoSelect.append('</optgroup>');
                        });
                        assuntoSelect.append('</optgroup>');
                    });
                },
                error: function() {
                    alert('Erro ao carregar assuntos.');
                }
            });
        } else {
            $('#assunto_codigo').empty();
            $('#assunto_codigo').append('<option value="">Selecione um Assunto Processual</option>');
        }
    });
});
