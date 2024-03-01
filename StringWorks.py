class StringNormalizer:

    def capitalizeFirstLetter(self, string: str):
        string = string[0].capitalize() + string[1:]
        return string

    def capitalizeEverFirstLetter(self, string: str):
        string = self.deleteExtraSpaces(string)
        if ' ' in string:
            words = string.split(' ')
            capitalize_words = []
            for word in words:
                capitalize_word = self.capitalizeFirstLetter(word)
                capitalize_words.append(capitalize_word)
            return ' '.join(capitalize_words)
        else:
            return string

    def formatNameToInitialsLastName(self, string: str):
        """Обязателен формат ФИО Фамилия Имя Отчество"""
        string = self.capitalizeEverFirstLetter(string)
        if string.count(' ') > 1:
            words = string.split(' ')
            return f'{words[1][0]}.{words[2][0]}.\xa0{words[0]}'
        else:
            return self.replaceSpacesByUnbreakable(string)

    def formatNameForSed(self, string: str):
        """Обязателен формат ФИО Фамилия Имя Отчество"""
        string = self.capitalizeEverFirstLetter(string)
        if string.count(' ') > 1:
            words = string.split(' ')
            return f'{words[0]} {words[1][0]}.{words[2][0]}'
        else:
            return self.replaceSpacesByUnbreakable(string)

    def deleteExtraSpaces(self, string: str):
        while '  ' in string:
            string = string.replace('  ', ' ')
        return string.strip()

    def replaceSpacesByUnbreakable(self, string):
        return string.strip().replace(' ', '\xa0')

    def removeSlashes(self, string: str) -> str:
        return string.replace('/', '-').replace('\\', '-')

    def prepareText(self, text: str):
        text = text.replace(' "', ' «').replace('" ', '» ').replace('".', '».').replace('",', '»,')
        return text.split('\n')


if __name__ == '__main__':
    result = StringNormalizer().formatNameForSed('орлов михаил сергеевич')

    print(result)
