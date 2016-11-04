import sqlite3

class DBAccess():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def add_image(image_name):
        command = "INSERT INTO images VALUES(?, ?, ?)"
        self.cursor.execute(command, (image_name, -1, 0))
        self.conn.commit()
    
    def add_total_section_count(image_name, total_count):
        command = "UPDATE images SET total_section_count = ? WHERE image_name = ?"
        self.cursor.execute(command, (total_count, image_name))
        self.conn.commit()
    
    def update_received_sections(image_name, received_sections):
        command = "UPDATE images SET received_sections = ? WHERE image_name = ?"
        self.cursor.execute(command, (received_sections, image_name))
        self.conn.commit()
    
    def add_image_section(image_name, section_num, section_text):
        command = "INSERT INTO image_sections VALUES(?, ?, ?)"
        self.cursor.execute(command, (image_name, section_num, section_text))
        self.conn.commit()
    
    def get_received_sections_count(image_name):
        command = "SELECT received_sections FROM images WHERE image_name = ?"
        self.cursor.execute(command, (image_name))
        return self.cursor.fetchone()[0]
    
    def get_total_sections_count(image_name):
        command = "SELECT total_section_count FROM images WHERE image_name = ?"
        self.cursor.execute(command, (image_name))
        return self.cursor.fetchone()[0]

    def get_image_sections(image_name):
        command = "SELECT section_text FROM image_sections WHERE image_name = ? ORDER BY section_num ASC"
        self.cursor.execute(command, (image_name))
        return self.cursor.fetchall()

    def delete_image_and_info(image_name):
        command1 = "DELETE FROM images WHERE image_name = ?"
        self.cursor.execute(command1, (image_name))
        command2 = "DELETE FROM image_sections WHERE image_name = ?"
        self.cursor.execute(command2, (image_name))
        self.conn.commit()
