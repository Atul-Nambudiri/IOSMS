import sqlite3

class DBAccess():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread = False)
        self.cursor = self.conn.cursor()

    def add_image(self, image_name):
        image_name = image_name.strip()
        image_name = image_name.strip()
        print("Image Name: %s" % (image_name,))
        command = "INSERT INTO images VALUES(?, ?, ?)"
        self.cursor.execute(command, (image_name, -1, 0))
        self.conn.commit()
    
    def add_total_section_count(self, image_name, total_count):
        image_name = image_name.strip()
        command = "UPDATE images SET total_sections_count = ? WHERE image_name = ?"
        self.cursor.execute(command, (total_count, image_name))
        self.conn.commit()
    
    def update_received_sections(self, image_name, received_sections):
        image_name = image_name.strip()
        command = "UPDATE images SET received_sections = ? WHERE image_name = ?"
        self.cursor.execute(command, (received_sections, image_name))
        self.conn.commit()
    
    def add_image_section(self, image_name, section_num, section_text):
        image_name = image_name.strip()
        command = "INSERT INTO image_sections VALUES(?, ?, ?)"
        self.cursor.execute(command, (image_name, section_num, section_text))
        self.conn.commit()
    
    def get_received_sections_count(self, image_name):
        image_name = image_name.strip()
        command = "SELECT received_sections FROM images WHERE image_name = ?"
        self.cursor.execute(command, (image_name,))
        return self.cursor.fetchone()[0]
    
    def get_total_sections_count(self, image_name):
        image_name = image_name.strip()
        command = "SELECT total_sections_count FROM images WHERE image_name = ?"
        self.cursor.execute(command, (image_name,))
        return self.cursor.fetchone()[0]

    def get_image_sections(self, image_name):
        image_name = image_name.strip()
        command = "SELECT section_text FROM image_sections WHERE image_name = ? ORDER BY section_num ASC"
        self.cursor.execute(command, (image_name,))
        return self.cursor.fetchall()

    def delete_image_and_info(self, image_name):
        image_name = image_name.strip()
        command1 = "DELETE FROM images WHERE image_name = ?"
        self.cursor.execute(command1, (image_name,))
        command2 = "DELETE FROM image_sections WHERE image_name = ?"
        self.cursor.execute(command2, (image_name,))
        self.conn.commit()
