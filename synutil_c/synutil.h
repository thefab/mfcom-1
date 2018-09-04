#ifndef SYNUTIL_H_
#define SYNUTIL_H_

#include <glib.h>

#define SYNUTIL_MAX(a,b) a>b?a:b
#define SYNUTIL_MIN(a,b) a<b?a:b

#define SYNUTIL_ANSI_COLOR_RESET       "\033[0m"
#define SYNUTIL_ANSI_COLOR_BLACK       "\033[30m"
#define SYNUTIL_ANSI_COLOR_RED         "\033[31m"
#define SYNUTIL_ANSI_COLOR_GREEN       "\033[32m"
#define SYNUTIL_ANSI_COLOR_YELLOW      "\033[33m"
#define SYNUTIL_ANSI_COLOR_BLUE        "\033[34m"
#define SYNUTIL_ANSI_COLOR_MAGENTA     "\033[35m"
#define SYNUTIL_ANSI_COLOR_CYAN        "\033[36m"
#define SYNUTIL_ANSI_COLOR_WHITE       "\033[37m"
#define SYNUTIL_ANSI_COLOR_BOLDBLACK   "\033[1m\033[30m"
#define SYNUTIL_ANSI_COLOR_BOLDRED     "\033[1m\033[31m"
#define SYNUTIL_ANSI_COLOR_BOLDGREEN   "\033[1m\033[32m"
#define SYNUTIL_ANSI_COLOR_BOLDYELLOW  "\033[1m\033[33m"
#define SYNUTIL_ANSI_COLOR_BOLDBLUE    "\033[1m\033[34m"
#define SYNUTIL_ANSI_COLOR_BOLDMAGENTA "\033[1m\033[35m"
#define SYNUTIL_ANSI_COLOR_BOLDCYAN    "\033[1m\033[36m"
#define SYNUTIL_ANSI_COLOR_BOLDWHITE   "\033[1m\033[37m"

#define SYNUTIL_ANSI_COLOR_OK          "\033[32;2m"
#define SYNUTIL_ANSI_COLOR_NORMAL      "\033[0;0m"
#define SYNUTIL_ANSI_COLOR_WARNING     "\033[33;2m"
#define SYNUTIL_ANSI_COLOR_ALERT       "\033[31;2m"
#define SYNUTIL_ANSI_COLOR_EMERGENCY   "\033[31;4m"

#define SYNUTIL_COLUMN_OK              60

void synutil_echo_ok(const gchar *message);
void synutil_echo_running();
void synutil_echo_nok(const gchar *message);
void synutil_echo_warning(const gchar *message);
void synutil_echo_bold(const gchar *message);
void synutil_echo_clean();
gchar *synutil_get_unique_hexa_identifier();
void synutil_g_free(gpointer pointer);

#endif /* SYNUTIL_H_ */
