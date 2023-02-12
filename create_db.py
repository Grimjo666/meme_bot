import sqlite3


def writing_info_to_bd(tg_id, name, username, text_count=0, voice_count=0, len_all_text=0, len_all_voice=0):

    base = sqlite3.connect('database/tg_meme_data.db')
    cur = base.cursor()

    base.execute('''CREATE TABLE IF NOT EXISTS tg_message_data(
                    id PRIMARY KEY,
                    name,
                    username,
                    text_count,
                    voice_count,
                    len_all_text,
                    len_all_voice)''')
    base.commit()

    cur.execute('''SELECT id, name, username FROM tg_message_data
                    WHERE id == ?''', (tg_id,))
    list_persons_info = cur.fetchone()

    if list_persons_info is None:
        cur.execute('''INSERT INTO tg_message_data (id, name, username, text_count, voice_count, len_all_text, len_all_voice)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tg_id, name, username, text_count, voice_count, len_all_text, len_all_voice))
        base.commit()

    elif list_persons_info == (tg_id, name, username):
        cur.execute('''UPDATE tg_message_data SET
                        text_count == text_count + ?,
                        voice_count == voice_count + ?,
                        len_all_text == len_all_text + ?,
                        len_all_voice == len_all_voice + ?
                        WHERE id == ?''', (text_count, voice_count, len_all_text, len_all_voice, tg_id))
        base.commit()
        base.close()
