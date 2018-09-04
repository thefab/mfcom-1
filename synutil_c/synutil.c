#include <glib.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <sys/stat.h>
#include <unistd.h>

#include "synutil.h"
#include "_synutil.h"

GRand *__rand = NULL;

GRand *__get_grand()
{
    if (__rand == NULL) {
        __rand = g_rand_new();
    }
    return __rand;
}

/**
 * Fonction qui retourne le timestamp courant
 *
 * @return timestamp courant
 */
glong synutil_get_current_timestamp()
{
    GTimeVal gtv;
    g_get_current_time(&gtv);
    return gtv.tv_sec;
}

/**
 * Retourne un identifiant "unique" sous forme d'une chaine hexa allouée
 *
 * @return identifiant "unique" hexa (à libérer par g_free)
 */
gchar *synutil_get_unique_hexa_identifier()
{
    GRand *rand = __get_grand();
    gchar *res = g_malloc(sizeof(gchar) * 33);
    guint32 ri;
    int i;
    for (i = 0 ; i < 4 ; i++) {
        ri = g_rand_int(rand);
        sprintf(res + (i * 8) * sizeof(gchar),  "%08x", ri);
    }
    return res;
}

void synutil_echo_clean()
{
    printf("%s%i%s", "\033[", SYNUTIL_COLUMN_OK, "G           ");
}

void synutil_echo_something(const gchar *code, const gchar *before, const gchar *after, const gchar *message, const gchar *line_end)
{
    printf("%s%i%s", "\033[", SYNUTIL_COLUMN_OK, "G");
    if ((message == NULL) || (strlen(message) == 0)) {
        printf("[ %s%s%s ]%s", before, code, after, line_end);
    } else {
        printf("[ %s%s%s ] %s%s", before, code, after, message, line_end);
    }
}

void synutil_echo_ok(const gchar *message)
{
    gboolean interactive = synutil_is_interactive_execution();
    if (interactive) {
        synutil_echo_clean();
        synutil_echo_something("OK", SYNUTIL_ANSI_COLOR_GREEN, SYNUTIL_ANSI_COLOR_NORMAL, message, "\n");
    } else {
        synutil_echo_something("OK", "", "", message, "\n");
    }
}

void synutil_echo_running()
{
    gboolean interactive = synutil_is_interactive_execution();
    if (interactive) {
        synutil_echo_clean();
        synutil_echo_something("RUNNING", SYNUTIL_ANSI_COLOR_YELLOW, SYNUTIL_ANSI_COLOR_NORMAL, NULL, "");
    }
}

void synutil_echo_nok(const gchar *message)
{
    gboolean interactive = synutil_is_interactive_execution();
    if (interactive) {
        synutil_echo_clean();
        synutil_echo_something("ERROR", SYNUTIL_ANSI_COLOR_RED, SYNUTIL_ANSI_COLOR_NORMAL, message, "\n");
    } else {
        synutil_echo_something("ERROR", "", "", message, "\n");
    }
}

void synutil_echo_warning(const gchar *message)
{
    gboolean interactive = synutil_is_interactive_execution();
    if (interactive) {
        synutil_echo_clean();
        synutil_echo_something("WARNING", SYNUTIL_ANSI_COLOR_YELLOW, SYNUTIL_ANSI_COLOR_NORMAL, message, "\n");
    } else {
        synutil_echo_something("WARNING", "", "", message, "\n");
    }
}

/**
 * Affiche un message en gras.
 */
void synutil_echo_bold(const gchar *message)
{
    printf("\033[1m%s\033[0m\n", message);
}

/**
 * Retourne TRUE si l'exécution du programme se fait dans un shell interactif et si stdout et stderr dirigent vers un terminal
 *
 * Si on redirige stdout et/ou stderr vers un pipe ou un fichier, la fonction retournera FALSE
 *
 * @return TRUE si l'exécution du programme se fait dans un shell interactif, FALSE sinon
 */
gboolean synutil_is_interactive_execution()
{
    gboolean res = TRUE;
    /*const gchar *tmp = g_getenv("PS1");
    if (tmp == NULL) {
        return FALSE;
    }*/
    const gchar *tmp2 = g_getenv("NOINTERACTIVE");
    if (tmp2 != NULL) {
        if (atoi(tmp2) == 1) {
            return FALSE;
        }
    }
    struct stat buf;
    if (stat("/tmp/nointeractive", &buf) == 0) {
        struct timespec tim = buf.st_mtim;
        if ((synutil_get_current_timestamp() - tim.tv_sec) < 60) {
            return FALSE;
        }
    }
    if (!(isatty(fileno(stdout)))) {
        return FALSE;
    }
    if (!(isatty(fileno(stderr)))) {
        return FALSE;
    }
    return res;
}

/**
 * Libère un pointer avec g_free
 *
 * Cette fonction est uniquement utile pour faire des bindings
 *
 * @param pointer pointeur à libérer
 */
void synutil_g_free(gpointer pointer)
{
    g_free(pointer);
}
