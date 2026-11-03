export default function CourseCard({ course, index, onEdit, onDelete }) {
  const instructorName = typeof course.instructor === 'object'
    ? course.instructor?.name
    : 'Course instructor';

  return <article className="course-card">
    <div className="course-cover"><span>{course.category || 'Course'}</span><strong>{['◒', '✳', '◉', '✦'][index % 4]}</strong></div>
    <div className="course-content">
      <div className="course-meta">{course.level || 'All levels'} · {course.duration || '—'} hours</div>
      <h3>{course.title}</h3>
      <p className="course-description">{course.description}</p>
      <div className="course-bottom"><span>{instructorName}</span><strong>{Number(course.price) === 0 ? 'Free' : `$${course.price}`}</strong></div>
      <div className="course-actions"><button onClick={() => onEdit(course)}>Edit</button><button onClick={() => onDelete(course._id || course.id)}>Delete</button></div>
    </div>
  </article>;
}
