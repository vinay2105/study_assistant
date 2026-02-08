from django.db import models

class Note(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    generated_notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Chunk(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    text = models.TextField()
    
    chunk_index = models.IntegerField()
    embedding = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'chunk_index')

    def __str__(self):
        return f"Chunk {self.chunk_index} of Note '{self.note.title}'"
    

class Chat(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat for Note '{self.note.title}' at {self.created_at}"

