/**
 * Binaire qui appelle la fonction synutil_echo_nok()
 *
 * @author Fabien MARTY <fabien.marty@meteo.fr>
 * @since avril 2012
 * @file echo_nok.c
 */

#include <glib.h>
#include "synutil.h"
#include <locale.h>
#include <stdio.h>

static GOptionEntry entries[] = {};

int main(int argc, char *argv[])
{
    /**
     * Variables globales
     */
    GError *error = NULL;
    GOptionContext *context;
    int res = 0;
    gchar *message = NULL;

    /**
     * Parsing de la ligne de commande
     */
    setlocale(LC_ALL, "");
    context = g_option_context_new("[MESSAGE] - write ERROR (with colors if supported) and a little optional message");
    g_option_context_add_main_entries(context, entries, NULL);
    if (!g_option_context_parse (context, &argc, &argv, &error)) {
        g_print(g_option_context_get_help(context, TRUE, NULL));
        fprintf(stderr, "ERROR WHEN COMMAND LINE PARSING\n");
    }
    if (argc > 2) {
        g_print(g_option_context_get_help(context, TRUE, NULL));
        fprintf(stderr, "ERROR WHEN COMMAND LINE PARSING\n");
    }
    if (argc == 2) {
        message = argv[1];
    }

    /**
     * Appel
     */
    synutil_echo_nok(message);

    /**
     * Libération / sortie
     */
    return res;
}
