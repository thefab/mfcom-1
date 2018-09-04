#ifndef _SYNUTIL_H_
#define _SYNUTIL_H_

#include <glib.h>

void synutil_echo_something(const gchar *code, const gchar *before, const gchar *after, const gchar *message, const gchar *line_end);
gboolean synutil_is_interactive_execution();

#endif /* _SYNUTIL_H_ */
