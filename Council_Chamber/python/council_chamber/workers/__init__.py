"""Local worker seats: ordinary local software, not language models.

These do the file operations, searches, builds, tests, and git
operations the spec says shouldn't cost an AI call -- each is a plain
class operating on a real project directory on disk.
"""
