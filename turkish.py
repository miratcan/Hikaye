# -*- coding: utf-8 -*-


llv_accusative_case_suffixes = {
    u'a': u'yı', u'e': u'yi', u'ı': u'yı', u'i': u'yi', u'o': u'yu',
    u'ö': u'yü', u'u': u'yu', u'ü': u'yü'
}

llo_accusative_case_suffixes = {
    u'a': u'i', u'e': u'i', u'ı': u'ı', u'i': u'i', u'o': u'u',
    u'ö': u'ü', u'u': u'u', u'ü': u'ü'
}

llv_genetive_case_suffixes = {
    u'a': u'nın', u'e': u'nin', u'ı': u'nın', u'i': u'nin', u'o': u'nun',
    u'ö': u'nün', u'u': u'nun', u'ü': u'nün'
}

llo_genetive_case_suffixes = {
    u'a': u'in', u'e': u'in', u'ı': u'ın', u'i': u'in', u'o': u'un',
    u'ö': u'ün', u'u': u'un', u'ü': u'ün'
}

vowels = u'aeıioöuü'


class Word(object):

    def __init__(self, word):
        assert type(word) == unicode, 'Words must be initialized with ' \
                                      'unicode strings.'
        self.word = word

    def get_last_vowel_info(self):
        """
        >>> assert Word(u'saat').get_last_vowel_info() == (False, 'a')
        >>> assert Word(u'puma').get_last_vowel_info() == (True, 'a')
        """
        w = self.word
        v = llv_accusative_case_suffixes
        lv = None
        for i in range(len(w) - 1, -1, -1):
            if w[i] in v:
                lv = w[i]
                break
        if not lv:
            return False, False
        if i == len(w) - 1:
            return True, lv
        return False, lv

    def bits(self):
        """
        Wovels are 1, consonants are 0.
        >>> assert Word(u'saat').bits() == '0110'
        """
        return ''.join(['1' if l in vowels else '0' for l in self.word])

    def syllables(self):
        """
        TODO: Add test here.
        """
        syllables = []
        word = self.word
        bits = self.bits()
        seperators = (('101', 1), ('1001', 2), ('10001', 2))
        index, cut_start_pos = 0, 0
        while index < len(bits):
            for seperator_pattern, seperator_cut_pos in seperators:
                if bits[index:].startswith(seperator_pattern):
                    cut_end_pos = index + seperator_cut_pos
                    syllables.append(word[cut_start_pos:cut_end_pos])
                    index += seperator_cut_pos
                    cut_start_pos = index
                    break
            index += 1
        syllables.append(word[cut_start_pos:])
        return syllables

    def add_suffix(self, suffix):
        """
        >>> assert Word(u'Kitap').add_suffix(u'a') == u'Kitaba'
        TODO: If K is last letter and N is before K, K softens to G.
        """
        if len(self.syllables()) == 1 or suffix[0] not in vowels:
            return self.word + suffix
        last_letter = self.word[-1]
        last_letter = {u'p': u'b', u'ç': u'c', u't': u'd', u'k': u'ğ'}\
            .get(last_letter, last_letter)
        return self.word[:-1] + last_letter + suffix

    def accusative(self):
        """
        >>> assert Word(u'saat').accusative() == u'saati'
        >>> assert Word(u'kitap').accusative() == u'kitabı'
        >>> assert Word(u'ağaç').accusative() == u'ağacı'
        >>> assert Word(u'kağıt').accusative() == u'kağıdı'
        >>> assert Word(u'saat').accusative() == u'saati'
        >>> assert Word(u'tarak').accusative() == u'tarağı'
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if is_vowel_last_letter:
            return self.word + llv_accusative_case_suffixes[vowel]
        else:
            return self.add_suffix(llo_accusative_case_suffixes[vowel])

    def genetive(self):
        """
        >>> assert Word(u'saat').genetive() == 'saatin'
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if is_vowel_last_letter:
            return self.word + llv_genetive_case_suffixes[vowel]
        else:
            return self.word + llo_genetive_case_suffixes[vowel]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
