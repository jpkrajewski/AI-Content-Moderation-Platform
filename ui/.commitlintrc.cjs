module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'subject-case': [2, 'always', 'sentence-case'],
        'subject-empty': [2, 'never'],
        'subject-full-stop': [2, 'never', '.'],
        'type-case': [2, 'always', 'lower-case'],
        'type-empty': [2, 'never'],
        'type-enum': [
            2,
            'always',
            [
                'build',
                'chore',
                'ci',
                'docs',
                'feat',
                'fix',
                'perf',
                'refactor',
                'revert',
                'style',
                'test'
            ]
        ],
        'body-leading-blank': [2, 'always'],
        'body-max-line-length': [2, 'always', 100],
        'footer-leading-blank': [2, 'always'],
        'header-max-length': [2, 'always', 72]
    },
};
