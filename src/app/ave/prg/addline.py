class AddLine():

    def add_line(self,s):
        new_s = s
        s_count = len(s)
        s_max_count = 15
        if s_count >= s_max_count:
            if (s_count - s_max_count) >= 3:
                # 15文字以上、かつ、2行目が3文字以上あれば、改行する
                # つまり、18文字以上であれば、15文字で改行する
                new_s = s[:s_max_count] + "\n" + s[s_max_count:]
        return new_s