#include <glib.h>
#include <glib/gprintf.h>
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
    context = g_option_context_new("- return a unique hexa identifier");
    g_option_context_add_main_entries(context, entries, NULL);
    if (!g_option_context_parse (context, &argc, &argv, &error)) {
        g_print(g_option_context_get_help(context, TRUE, NULL));
        fprintf(stderr, "ERROR WHEN COMMAND LINE PARSING\n");
        return 1;
    }

    /**
     * Appel
     */
    g_printf("%s\n", synutil_get_unique_hexa_identifier());

    /**
     * Libération / sortie
     */
    return res;
}
