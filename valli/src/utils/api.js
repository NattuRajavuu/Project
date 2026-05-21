export async function fetchProducts({ search = '', category = 'All', sort = 'featured' } = {}) {
  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (category && category !== 'All') params.set('category', category);
  if (sort && sort !== 'featured') params.set('sort', sort);

  const response = await fetch(`/api/products?${params.toString()}`);
  if (!response.ok) throw new Error('Unable to load products');
  return response.json();
}

export async function fetchProduct(id) {
  const response = await fetch(`/api/products/${id}`);
  if (!response.ok) throw new Error('Unable to load product');
  return response.json();
}
