/**
 * Binaire qui appelle la fonction synutil_echo_running()
 *
 * @author Fabien MARTY <fabien.marty@meteo.fr>
 * @since avril 2012
 * @file echo_running.c
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

    /**
     * Parsing de la ligne de commande
     */
    setlocale(LC_ALL, "");
    context = g_option_context_new("- write RUNNING (with colors if supported)");
    g_option_context_add_main_entries(context, entries, NULL);
    if (!g_option_context_parse (context, &argc, &argv, &error)) {
        g_print(g_option_context_get_help(context, TRUE, NULL));
        fprintf(stderr, "ERROR WHEN COMMAND LINE PARSING\n");
    }
    if (argc != 1) {
        g_print(g_option_context_get_help(context, TRUE, NULL));
        fprintf(stderr, "ERROR WHEN COMMAND LINE PARSING\n");
    }

    /**
     * Appel
     */
    synutil_echo_running();

    /**
     * Libération / sortie
     */
    return res;
}
